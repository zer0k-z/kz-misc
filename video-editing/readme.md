Useful resources:

- [HLAE](https://github.com/advancedfx/advancedfx): Very useful moviemaking tool.

- [Source Video Render](https://github.com/crashfort/SourceDemoRender): Produce movies for the Source engine with extreme performance.

- [SourceMod listen server for CSGO](https://houseofclimb.com/threads/csgo-listen-server-with-kztimer.1106/): Follow the first 3 steps only. KZTimer not required. Use this along with SVR.

- [CVar Unlocker](https://forums.alliedmods.net/showpost.php?p=796981&postcount=4): Sourcemod plugin, use this along with the listen server to unlock hidden cvar/commands. Need to open a map first!

- [Demoinfogo](https://github.com/WeavrTV/csgo-demoinfo): Include build script using Visual Studio 2019. Use its output along with VS2019 debug mode to modify demo content.

- [HxD](https://mh-nexus.de/en/hxd/): Hex editor, use with demoinfogo in VS2019 debug mode to modify demos.

- [HLAE material picker tutorial](https://www.youtube.com/watch?v=7Mnbr-3RvPs): Use to find material, good to find materials to hide with `mat_suppress`.

- [BSPSource](https://github.com/ata4/bspsrc): Map decompiler. Sometimes you need to recompile maps to add specific effects or fix some visual bugs in old maps.

Useful commands:

- mat_suppress: CSGO hidden command, require `mirv_cvar_unhide_all` in HLAE or CVar Unlocker to use.

- mat_autoexposure_max_multiplier: Change the max autoexposure value in HDR maps.

- mat_bloomamount_rate: Just like the name suggests, bloom amount.

- mat_accelerate_adjust_exposure_down: Allegedly makes bloom adjustment less agressive

- mat_debug_bloom: Bloom debug, use with `developer 2`.

