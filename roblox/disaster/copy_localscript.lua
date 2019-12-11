wait(3)
local tool = script.Parent
local player = game.Players.LocalPlayer
local mouse = player:GetMouse()
local clickEvent = tool.ClickEvent

local function onActivate()
	local clickTarget = mouse.Target
	print(clickTarget.Name)
	clickEvent:FireServer(clickTarget)
end

tool.Activated:connect(onActivate)