local tool = script.Parent
local clickEvent = tool.ClickEvent
local clickEventConnection
local function clonePart(oldpart)
	if (oldpart ~= game.workspace.Spawn and oldpart ~= game.workspace.Baseplate and (oldpart.Parent == game.workspace.BuildBlocks or oldpart.Name == tool.Parent.Name))then
		local newpart = oldpart:Clone()
		newpart.Name = tool.Parent.Name
		newpart.Position = oldpart.Position + Vector3.new(0, oldpart.Size.y, 0)
		newpart.Parent = workspace
		newpart.Anchored = true
		newpart.Locked = false
	end
end

local function onClick(player, clickTarget)
	clonePart(clickTarget)
end

local function onEquip()
	clickEventConnection = clickEvent.OnServerEvent:connect(onClick)
end

local function onUnequip()
	clickEventConnection:disconnect()
end

tool.Equipped:connect(onEquip)
tool.Unequipped:connect(onUnequip)	