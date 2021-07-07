// Script to animate player speed and takeoff using speed.csv from gokz-replays-speedtotext

// Text / Source Text / Expression: Source Text
t = Math.floor((time)*128);
if ((t>0)&&(t<5366)) // Lazy hardcode, 5366 is the demo tick count
{
    footage("speed.csv").dataValue([0,t]);  //[1,t] for takeoff speed
} else
{
    footage("speed.csv").dataValue([0,5366]); // Same change here for takeoff speed
}

// Animator / Fill Color / Expression: Fill Color

t = Math.floor((time)*128);
if ((t>0)&&(t<5366)&&footage("speed.csv").dataValue([2,t]) == 0) // Lazy hardcode, 5366 is the demo tick count
{
    [1,1,1,1] // White
}
else [0,1,0,1] // Green