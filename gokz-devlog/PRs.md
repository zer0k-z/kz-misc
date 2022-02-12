## Replay Bot Name Fix

This is my first GOKZ pull request.

Previously the bot's name will not update on the client side upon using the replay function and will only works when the client changes their spectating mode. So I create a timer that forcibly changes the spectating mode of the spectating client.

This is not a great solution, it causes a few bugs such as replay bot abruptly ends the moment it starts. 

I should make some changes when the new replay system comes out. In the mean time digging into the source code and finding out the underlying function behind updating spectated player's name seems to be the best course of action.

## Add bonus maptop commands

Very basic pull request, it just adds a few more command aliases for checking bonus top.

## Spectating name filter

Previously when you use the `!spec` command, if it finds more than one match then it would return an error and stops. With this pull request, instead of stopping entirely, it now acts as a filter and the user can now choose one of the players that matches this text filter.

## Allow self-spectating in free look mode

Previously self-spectating is very annoying with `!spec`. The command would return an error if the user use their own name as an argument.

While it's possible to self-spectate using it without any argument, this was only possible if the server is empty, and even so the movement control was unintuitive in CSGO as you have to enter the right observer mode in order to move around (basically pressing +jump with no visual indicator until you get to move around freely)


By looking for `@me` argument, the command now can put the observer in free look mode instead of returning an error. Useful if the player wants to look around themselves in the middle of a run. 

## Allow painting for spectators

Another simple pull request. The old paint plugin checks for whether the player is alive before doing paints. Now it doesn't anymore.

## Fix !specs returning unknown command

Very simple pull request. Commands should return `Plugin_Handled` eventually to prevent this error. By default this returns `Plugin_Continue`.

## Fix pipeline errors

Apparently the `i386` image of Alpine does not work anymore because of the architecture difference (pipeline is run on `x86_64`).

However, `libc6-compat` breaks on `x86_64`, so `gcompat` is used instead.

Alpine does not support running 32-bit applications on a 64-bit architecture because it does not have `multilib` support, so `spcomp64` is used for compiling instead.

## Rebalance SKZ jumpstats tiers due to bhop height changes

This will only adjust bhop and multi bhop tiers, as their jump heights are nerfed.

Weirdjump tiers and jumpbug tiers are not affected. The reason is WJ prespeed can be significantly higher than the max prestrafe value (281-ish), and jumpbug height was not affected by the SKZ height nerf (when this PR was merged)

## GOTV chat fix

Previously, KZ servers using demos do not contain chat information.

This is caused by `CPrintToChat` not sending to GOTV/SourceTV clients.

A side effect of this is that things such as `gokz-tips` would be spamming the GOTV client. So I added a condition to prevent this from happening.

## Fix laser not appearing in jumpbeam and measure

It was using materials that do not (anymore?) exist in the game.

Seeing that there is an equivalent of these materials already in the game and they even have a better quality, I just do a simple switch and rescale them properly.

## Fix broken third person animation for bots

GOKZ uses the old models because the new model has very annoying bobbing animations. Replay bots do not like this and will have frozen/broken animations. So I opted to use the new models for the bots, as bots are conveniently the exception to this bobbing issue.

## Fix jumpstats invalidating when hitting a block's edge

Previously jumps will become invalid if it hits anything. This doesn't make a whole lot of sense because most of the time when you collide with something it only slows you down, unless it is something that can accelerate you (but when does that happen?). Just to be sure, I make sure that the invalidation only happens when you somehow speed up from the collision.

## Nerf the ability to checkpoint on teleport triggers

A few years ago the minimum bhop trigger delay is 0.15s, but this was changed to 0.11 because I complained about the huge checkpoint delay on non-bhop blocks.

This has proven to be a mistake, as the timer inconsistency can cause the usual 0.109375s teleport delay to increase by a few ticks, allowing player to occasionally checkpoint on bhop blocks. Having low fps, or previously having `cl_updaterate 64` can increase the teleport delay as well. And some bhop triggers are more inconsistent than others depending on maps.

This PR should make it very hard to make checkpoints on bhop blocks, decrease the success chance from to almost 0.05% from my personal testing, making this strategy wildly inefficient.

This change might be controversial however, as it means that runs that relying on checkpoint on bhop blocks become impossible. I would argue that they should never be possible in the first place, and any sort of bhop checkpoint should be fixed.

## Hook CCSPlayer::Spawn to correct ground flags

Upon spawning, the game adds `FL_ONGROUND` flag to the player, regardless of whether they are actually on the ground or not. This leads to several issues, the biggest one being able to checkpoint in the air.

`SetGroundEntity(NULL)` is called all the time in the air but it doesn’t reset the flag because the game thinks that nothing has changed and immediately returns.

The player_spawn event is too early to update ground flag, so `CCSPlayer::Spawn` is used instead.

## Do not react upon externally created round_start events

External plugins that record GOTV demos can call `round_start` event to fix demo corruption, which happens to stop the players' timer. GOKZ should only react on real round start events only.

## Fix IsClientSourceTV returning error for index 0

Apparently `IsClientSourceTV()` doesn't like console client index, so there are errors that show up when using chat commands through console, as the client is the console.

## Fix gamedata file name for velmod-fix PR

The only reason it is worth mentioning is that gamedata file name is case sensitive on Linux and not on Windows… 

## Adjust edge calculation

When a trace hit something, it moves 0.03125 unit away from the actual destination. Edge calculation now take this value into account.

I still feel like this doesn't seem to be quite correct. It introduces some bugs where a jump shouldn't be a block jump, and maybe there's some cases where 0.03125 is no the correct offset. Might be worth investigating later.

Sometimes you are able to land while being 0.03125 units ahead of the block itself. The block trace needs to be extended so it can hit the block when that happens.

## Demo Record Fix

Allow players to record pov demos with `record` in console. This will put the server in permanent warmup, but `gokz_demofix` is added to disable this feature.

I also fix demo corruption by sending a fake `round_start` event to the client once the recording starts. Without this, the demo will be unplayable.

## Fix custom models temporarily changing player collisions

Custom models can change player collisions for just long enough (like 1 tick) to activate triggers through walls. I make sure that the models collisions stay the same after changing to prevent abuses.

## Fix players getting kicked/spawning in the void

The plugin now assigns player to a team upon joining, this should stop the bug where you get kicked out of the server if you don’t choose any team. This also fixes (hopefully) the bug where you can accidentally change team while the change team panel is not visible. 

A valid spawn check is added upon adding new spawns. A spawn is valid if it’s in bounds and not stuck inside the ground.

Player’s origin is moved to a valid spawn point upon (re)spawning.

## Allow player to (somewhat) press button through players

There are two ways player can press a button, either through a direct trace to the button or a sphere around the player’s eyes. 

When the button press trace hits a player, another trace is fired and this one ignores all players to find a button.

This fix only contains the direct trace method, the other method would be difficult to implement before SourceMod 1.11.

## Remove drown damage sounds

After digging around the leaked source code, this is possible simply by adding `FL_GODMODE` flag to players. I think `FL_GODMODE` should already prevent you from taking any damage, but I just kept `m_takedamage` stuff there just in case.

## Prevent speed abuse with glove plugins

If the player runs faster than 250 speed, it should be capped back to 250 in VNL. This stops gloves from briefly giving players 260 maxspeed as it temporarily removes the player’s weapon, setting their speed to 260.

## Remake gokz-measure structure, add +measure and !measureblock

As the title says, `+measure` is a simply a click-and-drag solution without having to use `!measure`. `!measureblock` is a menu option inside `!measure` menu, now copied to a standalone command.

