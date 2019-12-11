local Tool = script.Parent

enabled = true

local selectionBox
local selectionLasso
local handles

local previousDistance

function onHandlesDown(normal)
	print("handlesDown")
	previousDistance = 0
end
function onHandlesDrag(normal, distance)
	
	if handles.Adornee then
		local delta = distance - previousDistance 
		if math.abs(delta) >= handles.Adornee.ResizeIncrement then
			local sizeDelta = math.floor(delta / handles.Adornee.ResizeIncrement + 0.5) * handles.Adornee.ResizeIncrement
			if handles.Adornee:Resize(normal, sizeDelta) then
				previousDistance = distance
			end
		end
	end
end

function onButton1Down(mouse)
	print("3DButtonDown")
	if mouse.Target == nil or mouse.Target.Locked  or (Tool.Parent.Name ~= mouse.Target.Name)then
		selectionBox.Adornee = nil
		selectionLasso.Part = nil
		handles.Adornee = nil
	else
		selectionBox.Adornee = mouse.Target
		selectionLasso.Part = mouse.Target
		handles.Adornee = mouse.Target
		handles.Faces = mouse.Target.ResizeableFaces
	end
end



function onEquippedLocal(mouse)
	mouse.Button1Down:connect(function() onButton1Down(mouse) end)

	local character = script.Parent.Parent
	local player = game.Players:GetPlayerFromCharacter(character)
	
	selectionBox = Instance.new("SelectionBox")
	selectionBox.Color = BrickColor.Yellow()
	selectionBox.Adornee = nil
	selectionBox.Parent = player.PlayerGui

	selectionLasso = Instance.new("SelectionPartLasso")
	selectionLasso.Name = "Model Delete Lasso"
	selectionLasso.Humanoid = character.Humanoid
	selectionLasso.Parent = game.workspace
	selectionLasso.Part = nil
	selectionLasso.Visible = true
	selectionLasso.archivable = false
	selectionLasso.Color = BrickColor.Black()

	handles = Instance.new("Handles")
	handles.Color = BrickColor.White()
	handles.Adornee = nil
	handles.MouseDrag:connect(onHandlesDrag)
	handles.MouseButton1Down:connect(onHandlesDown)
	handles.Parent = player.PlayerGui
end

function onUnequippedLocal()
	selectionBox:Remove()
	selectionLasso:Remove()
	handles:Remove()
end


Tool.Equipped:connect(onEquippedLocal)
Tool.Unequipped:connect(onUnequippedLocal)
