-- gm_grand_central screenshot rig. Runs only when data/gcs_shots_go.txt exists
-- (tools/shots.sh writes it); captures each camera to data/gcs_shots/, then quits.
if SERVER then return end
if not file.Exists("gcs_shots_go.txt", "DATA") then return end
if game.GetMap() ~= "gm_grand_central" then return end
file.Delete("gcs_shots_go.txt")
file.CreateDir("gcs_shots")

local CAMS = {
  { "west_balcony", Vector(-1500, 0, 400), Angle(5, 0, 0) },
  { "floor_east",   Vector(-1200, -500, 72), Angle(-15, 20, 0) },
  { "booth",        Vector(-500, 300, 120), Angle(0, -30, 0) },
  { "clock",        Vector(-320, -60, 120), Angle(-8, 10, 0) },
  { "board",        Vector(150, 0, 150), Angle(-10, -95, 0) },
  { "flag",         Vector(0, -300, 72), Angle(-42, 90, 0) },
  { "vault_up",     Vector(-600, 0, 72), Angle(-70, 0, 0) },
  { "east_balcony", Vector(1500, 0, 400), Angle(5, 180, 0) },
  { "stairs_west",  Vector(-700, -300, 72), Angle(-5, 160, 0) },
  { "arcade_west",  Vector(-1480, 0, 80), Angle(-6, 180, 0) },
  { "balc_arcade",  Vector(-1450, 140, 380), Angle(-2, 180, 0) },
  { "ramp_head",    Vector(-950, 390, 90), Angle(12, 180, 0) },
  { "ramp_down",    Vector(-1900, 390, -40), Angle(8, 180, 0) },
  { "east_ramp",    Vector(950, -390, 90), Angle(12, 0, 0) },
  { "east_down",    Vector(1900, -390, -40), Angle(8, 0, 0) },
  { "east_land",    Vector(2750, 300, -200), Angle(5, -60, 0) },
  { "whisper",      Vector(-2720, -300, -200), Angle(-12, 155, 0) },
  { "oyster",       Vector(-3420, -380, -200), Angle(-4, 170, 0) },
  { "dining",       Vector(-960, -400, -200), Angle(-4, 20, 0) },
  { "ob_entry",     Vector(-2780, 0, -210), Angle(-6, 180, 0) },
  { "dining_clock", Vector(-220, -160, -190), Angle(4, 35, 0) },
  { "vh_door",      Vector(-1302, -400, 90), Angle(0, -90, 0) },
  { "vanderbilt",   Vector(-1480, -1180, 90), Angle(-12, -15, 0) },
  { "vh_east",      Vector(700, -1450, 90), Angle(-8, 180, 0) },
  { "vh_42nd",      Vector(-360, -1150, 90), Angle(-2, -90, 0) },
  { "ob_counter",   Vector(-3600, 300, -200), Angle(-6, 200, 0) },
}
local i, cam, frames = 0, nil, 0
local ft, fpslog = 0, {}  -- frame time summed over frames 31-89, one fps line per camera

hook.Add("CalcView", "gcs_shots", function()
  if cam then return { origin = cam[2], angles = cam[3], fov = 90, drawviewer = false } end
end)
hook.Add("HUDShouldDraw", "gcs_shots", function() if cam then return false end end)
hook.Add("PostRender", "gcs_shots", function()
  if not cam then return end
  frames = frames + 1
  if frames > 30 then ft = ft + RealFrameTime() end
  if frames < 90 then return end
  fpslog[#fpslog + 1] = string.format("%-14s %4.0f fps", cam[1], 59 / math.max(ft, 1e-4))
  ft = 0
  local data = render.Capture({ format = "jpg", quality = 92, x = 0, y = 0, w = ScrW(), h = ScrH() })
  file.Write("gcs_shots/" .. cam[1] .. ".jpg", data)
  i, frames = i + 1, 0
  cam = CAMS[i]
  if not cam then
    file.Write("gcs_shots/fps.txt", table.concat(fpslog, "\n") .. "\n")
    file.Write("gcs_shots/done.txt", "done")
    timer.Simple(1, function() RunConsoleCommand("quit") end)
  end
end)
timer.Simple(8, function()
  RunConsoleCommand("mat_autoexposure_max", "1.5")
  i = 1; cam = CAMS[1]
end)
