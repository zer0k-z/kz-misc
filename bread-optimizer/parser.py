import time
from bs4 import BeautifulSoup
import requests
import pandas
import socket
import os
from multiprocessing import Pool, Lock

def init(l):
	global lock
	lock = l

def get_map_info(map_name):
	print(str(os.getpid()) + ': Parsing map ' + map_name + "...")
	map_url = 'https://loafofbread.cf/maps.php?name={name}'.format(name = map_name)
	r = requests.get(map_url)
	data = r.text
	soup = BeautifulSoup(data, 'html.parser')
	# Tier
	span = soup.find_all("span", {'class':'globalStatusSpan'})
	tier = span[0].get_text()
	if tier != 'Non Global':
		tier = span[2].get_text()
	# WR
	span = soup.find_all("span", {'class':'recordPro'})
	pro_wr = span[0].get_text()
	span = soup.find_all("span", {'class':'recordNub'})
	nub_wr = span[0].get_text()
	nub_wr = nub_wr.replace('(','').replace(')','')
	# Avg time
	span = soup.find_all("td", {'class':"tdEntryMaps tdDark"})
	avg_time = span[1].get_text().split(': ')[1]
	# Completion counts
	tp_completions = span[0].get_text().split(': ')[1]
	pro_completions = span[2].get_text().split(': ')[1]
	# critical section
	lock.acquire()
	with open("maps.txt", "a+", encoding='utf-8') as f:
		print("{id}: {name}, {tier}, {avg_time}, {tp_completions}, {nub_wr}, {pro_completions}, {pro_wr}".format(id = os.getpid(), name = map_name, tier = tier, avg_time = avg_time, tp_completions = tp_completions, pro_completions = pro_completions, pro_wr = pro_wr, nub_wr = nub_wr))
		f.write("{name}, {tier}, {avg_time}, {tp_completions}, {nub_wr}, {pro_completions}, {pro_wr}\n".format(name = map_name, tier = tier, avg_time = avg_time, tp_completions = tp_completions, pro_completions = pro_completions, pro_wr = pro_wr, nub_wr = nub_wr))
	lock.release()

if __name__ == "__main__":
	lock = Lock()
	start_lock = Lock()
	site = pandas.read_html('https://loafofbread.cf/players.php?sid32=158416176')
	map_list = site[7]['Map'].tolist()
	print('Request done!')
	if map_list is not None:
		if os.path.exists("maps.txt"):
			os.remove("maps.txt")
		with open("maps.txt", "a+", encoding='utf-8') as f:
			f.write("name, tier, avg_time, tp_completions, nub_wr, pro_completions, pro_wr\n")
		p = Pool(6, initializer=init, initargs=(lock,))
		p.map_async(get_map_info, map_list)
		p.close()
		p.join()
	else:
		print('[!] Request Failed')
