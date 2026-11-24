-- gm_grand_central screenshot rig. Runs only when data/gcs_shots_go.txt exists
-- (tools/shots.sh writes it); captures each camera to data/gcs_shots/, then quits.
if SERVER then return end
if not file.Exists("gcs_shots_go.txt", "DATA") then return end
if game.GetMap() ~= "gm_grand_central" then return end
file.Delete("gcs_shots_go.txt")
file.CreateDir("gcs_shots")

local CAMS = {
  { "vest_out",     Vector(-360, -1972, 64), Angle(-3, -90, 0) },
  { "ext_door",     Vector(-360, -2616, 64), Angle(-8, 90, 0) },
  { "ext_street",   Vector(-360, -3516, 72), Angle(-28, 90, 0) },
  { "ext_clock",    Vector(-2076, -3100, 352), Angle(-37, 25, 0) },
  { "ext_viaduct",  Vector(-2076, -3400, 352), Angle(-5, 90, 0) },
  { "ext_west",     Vector(2200, -2900, 72), Angle(-10, 180, 0) },
  { "ext_terrace",  Vector(1300, -2316, 352), Angle(0, 180, 0) },
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
