local tool = script.Parent
local clickEvent = tool.ClickEvent
local clickEventConnection

local function removePart(part)
	if not part.Locked and part.Parent.Name~="BuildBlocks" and (part.Name == tool.Parent.Name)then
		part:Destroy()
	end
end

local function onClick(player, clickTarget)
	removePart(clickTarget)
end

local function onEquip()
	clickEventConnection = clickEvent.OnServerEvent:connect(onClick)
end

local function onUnequip()
	clickEventConnection:disconnect()
end

tool.Equipped:connect(onEquip)
tool.Unequipped:connect(onUnequip)	