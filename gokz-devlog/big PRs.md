

## Change how velocity modifier is applied to players

Using `m_flVelocityModifier` to modify player ground speed leads to two issues:

1. Player loses ground speed when they switch to a slower weapon. This is caused by `m_flVelocityModifier` being updated too early, before the game actually updates the player's weapon.

It’s easy to verify this by giving yourself a negev and switching back and forth between it and the knife.

2. When the player duckbugs, `m_flVelocityModifier` is not applied until it is too late.

`CCSGameMovement::CheckParameters()` is responsible for applying `m_flVelocityModifier` to player's maxspeed, this is only done if the player is on ground, which can be true if the player unducks on this tick.

However, `CheckParameters()` is called before `CCSGameMovement::Duck()`, which is called before `CGameMovement::WalkMove()`.

Therefore, if `Duck()` is called and the player is no longer airborne, `WalkMove()` will then clamp the player velocity to their maxspeed (which at that point isn't yet affected by `m_flVelocityModifier`).

This can be seen when players successfully do a duckbug but miss a jump by one tick, they will take off with prespeed smaller or equal to their weapon’s max speed.

Hooking `CCSPlayer::GetPlayerMaxSpeed()` and using it as the prestrafe velocity modifier would fix both of these issues.

The call order is as following:

```
OnPlayerRunCmd <- GOKZ calls TweakVelMod() here
CCSPlayer::PlayerRunCommand()
  CBasePlayer::PlayerRunCommand()
    CPlayerMove::RunCommand()
      player->SelectItem(weapon->GetName(), ucmd->weaponsubtype) <- Only here the weapon gets updated
      g_pGameMovement->ProcessMovement()
        mv->m_flMaxSpeed = pPlayer->GetPlayerMaxSpeed();
        CGameMovement::PlayerMove()
          CCSGameMovement::CheckParameters() <- Only multiply m_flMaxSpeed by m_flVelocityModifier if the player is on the ground
          CCSGameMovement::Duck() <- Can set player to the ground and call FullWalkMove() instead
          CGameMovement::FullWalkMove()
          CGameMovement::WalkMove() <- Velocity clamp
```


## Better saveloc, change blockable native behavior, rework checkpoint storage

Checkpoint storage is rewritten as `ArrayList` of enum struct, this makes it easier for saveloc to include checkpoints. Using `ArrayList` for checkpoint can reduces memory size as well, though this makes it slightly slower but this should not be noticeable. Perhaps the better way should be using `ArrayStack` but it is missing a lot of functionalities for whatever reason.

Various natives are added for saveloc. Some externally called natives used to be blocked by `gokz-global`, now they will invalidate player’s run instead.

Saveloc now includes gokz data (running timer, tp count). Upon finishing a saveloc’d run, only the saveloc player will see the saveloc’d time, as the run was not valid.

Saveloc now includes precise duck related variables, preventing players from being stuck with loadloc.

I hope to be able to import/export locs someday, preferably using base64 or something like that. But it seems like checkpoints can't be exported because they will take up too much storage, if this ever becomes a reality.

# MovementAPI 3.0

The most important thing that MovementAPI 3.0 bring is mid-movement processing hooks. Previously movement modifications are always 1 tick too late as it can only reacts before or after movement processing, which won't be the case anymore!

3.0 hooks the movement processing functions themselves, so it is much more precise in terms of timing. This should fix weirdness with KZT and SKZ perf cap sometimes not working.

This also comes with major changes towards various GOKZ modules, such as...

## VNL

The hardcoded bhop/jb speed cap is now gone, because we can get the precise takeoff velocity now.

## KZT/SKZ

Caps the player bhop speed the moment they jump instead of one tick too late, also to apply slopefix right after landing to work with jumpbugs.

## Jumpstats

Ladderhop jumpstats with height offset no longer registers, hopefully.

Change how bhop height is calculated, now treat jumpbugs almost the same way as bhops by listening to the same forward.

Slightly rearrange jump tracking function order.

Jumptracking now truly reflects changes to player’s velocity, no more bogus prespeed from jumpbugs on KZT/SKZ.

It now accurately invalidates any jump invalidated by gokz-core as jumps were getting invalidated by SetVelocity on perfs.