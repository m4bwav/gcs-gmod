-- gm_grand_central escalator ride test, installed by tools/walk.sh only. Runs when data/gcs_walk_go.txt
-- exists: puts the player on each MetLife escalator lane (build_vmf.py ESC_*), either standing still
-- (ride) or holding +forward against the lane, and logs where it ended to data/gcs_walk/result.txt.
if game.GetMap() ~= "gm_grand_central" then return end
if not file.Exists("gcs_walk_go.txt", "DATA") then return end
file.Delete("gcs_walk_go.txt")
file.CreateDir("gcs_walk")
local ROUTES = {  -- name, start, yaw, seconds, end height to reach, hold forward
  { "ride_up",          Vector(820, 614, 8), 0, 10, 308, false },
  { "ride_down",        Vector(1410, 530, 320), 180, 10, 4, false },
  { "walk_up_the_down", Vector(820, 530, 8), 0, 12, 308, true },
  { "walk_down_the_up", Vector(1410, 614, 320), 180, 12, 4, true },
  { "vl_ride_up",       Vector(-2360, 56, 8), 180, 10, 236, false },
  { "vl_ride_down",     Vector(-2940, -56, 248), 0, 10, 4, false },
  { "vl_walk_up_down",  Vector(-2360, -56, 8), 180, 10, 236, true },
  { "md_ride_down",     Vector(-636, -970, -256), 270, 18, -968, false },
  { "md_ride_up",       Vector(-428, -2260, -964), 90, 18, -268, false },
  { "md_walk_up_down",  Vector(-636, -2260, -964), 90, 18, -268, true },
}
local out, cur, ply, t0 = {}, nil, nil, 0
hook.Add("StartCommand", "gcs_walk", function(p, cmd)
  if cur and p == ply then
    cmd:ClearButtons(); cmd:SetSideMove(0); cmd:SetViewAngles(Angle(0, cur[3], 0))
    if cur[6] then cmd:SetButtons(IN_FORWARD); cmd:SetForwardMove(200) else cmd:SetForwardMove(0) end
  end
end)
local function run(i)
  cur = ROUTES[i]
  if not cur then
    file.Write("gcs_walk/result.txt", table.concat(out, "\n") .. "\n")
    file.Write("gcs_walk/done.txt", "done")
    return
  end
  ply:SetPos(cur[2]); ply:SetEyeAngles(Angle(0, cur[3], 0)); ply:SetVelocity(-ply:GetVelocity())
  t0 = CurTime()
  local reached
  timer.Create("gcs_walk_poll", 0.1, 0, function()
    local p = ply:GetPos()
    if not reached and ((cur[5] > cur[2].z and p.z >= cur[5]) or (cur[5] < cur[2].z and p.z <= cur[5])) then
      reached = CurTime() - t0
    end
  end)
  timer.Simple(cur[4], function()
    timer.Remove("gcs_walk_poll")
    local p = ply:GetPos()
    out[#out + 1] = string.format("%-17s %s  end (%.0f, %.0f, %.0f), wanted z %s %d, reached after %s s", cur[1],
      reached and "PASS" or "FAIL", p.x, p.y, p.z, cur[5] > cur[2].z and ">=" or "<=", cur[5],
      reached and string.format("%.1f", reached) or "-")
    run(i + 1)
  end)
end
timer.Simple(10, function() ply = Entity(1); if IsValid(ply) then run(1) end end)
