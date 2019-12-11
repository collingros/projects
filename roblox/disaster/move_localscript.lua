local Tool = script.Parent

enabled = true
local origTexture = 	Tool.TextureId
local selectionBox
local currentSelection
local currentSelectionColors = {}
local selectionLasso
local inGui = false
local inPalette = false
local lockTime = 0
local tool = script.Parent

function canSelectObject(part)
	return part and not (part.Locked) and (part.name == tool.Parent.Name)  and (part.Position - script.Parent.Parent.Head.Position).Magnitude < 60
end

function findModel(part)
	while part ~= nil do
		if part.className == "Model" then
			return part
		end
		part = part.Parent
	end

	return nil
end


function startDrag(mousePart, hitPoint, collection)
	dragger = Instance.new("Dragger")
	pcall(function() dragger:MouseDown(mousePart, hitPoint, collection) end)
end

function collectBaseParts(object, collection)
	if object:IsA("BasePart") then
		collection[#collection+1] = object
	end
	for index,child in pairs(object:GetChildren()) do
		collectBaseParts(child, collection)
	end
end

function onMouseDown(mouse) 

	local part = mouse.Target
	if canSelectObject(part) then
		local hitPoint = mouse.Hit:toObjectSpace(part.CFrame).p
		if trySelection(part) then
			local instances = {}
			collectBaseParts(currentSelection, instances)
			startDrag(part, hitPoint, instances)
			return
		end
	end

	onMouseUp(mouse)
end



function onMouseUp(mouse)
	if dragger ~= nil then
		pcall(function() dragger:MouseUp() end)
		dragger = nil
	end
end

function trySelection(part)
	if canSelectObject(part) then
		selectionLasso.Part = part
		local model = findModel(part)
		if model then 		
			return setSelection(model)
		else
			return setSelection(part)
		end
	else
		clearSelection()
		return false
	end
end

function onKeyDown(key)
	if dragger ~= nil then
		if key == 'R' or key == 'r'  then
			dragger:AxisRotate(Enum.Axis.Y)
		elseif key == 'T' or key == 't' then
			dragger:AxisRotate(Enum.Axis.Z)
		end
	end
end
local alreadyMoving
function onMouseMove(mouse)
	if alreadyMoving then
		return
	end

	alreadyMoving = true
	if dragger ~= nil then
		if time() - lockTime > 3 then
			Instance.Lock(currentSelection)
			lockTime = time()
		end
		
		pcall(function() dragger:MouseMove(mouse.UnitRay) end)
	else
		trySelection(mouse.Target)
	end
	alreadyMoving = false
end



	
function setSelection(partOrModel)
	if partOrModel ~= currentSelection then
		clearSelection()
		if Instance.Lock(partOrModel) then
			lockTime = time()
			currentSelection = partOrModel
			selectionBox.Adornee = currentSelection
			return true
		end
	else
		if currentSelection ~= nil then
			if time() - lockTime > 2 then
				if not(Instance.Lock(currentSelection)) then
					clearSelection()
					return false
				else
					lockTime = time()
					return true
				end
			else
				return true
			end
		end
	end

	return false
end

function clearSelection()
	if currentSelection ~= nil then
		for part, color in pairs(currentSelectionColors) do
			part.BrickColor = color
		end
		selectionBox.Adornee = nil
		Instance.Unlock(currentSelection)
	end
	currentSelectionColors = {}
	currentSelection = nil
	selectionLasso.Part = nil
	selectionBox.Adornee = nil
end

function onEquippedLocal(mouse)

	local character = script.Parent.Parent
	local player = game.Players:GetPlayerFromCharacter(character)
	guiMain = Instance.new("ScreenGui")
	guiMain.Parent = player.PlayerGui

	inGui = false
	inPalette = false


	mouse.Button1Down:connect(function() onMouseDown(mouse) end)
	mouse.Button1Up:connect(function() onMouseUp(mouse) end)
	mouse.Move:connect(function() onMouseMove(mouse) end)
	mouse.KeyDown:connect(function(string) onKeyDown(string) end)

	selectionBox = Instance.new("SelectionBox")
	selectionBox.Name = "Model Delete Selection"
	selectionBox.Color = BrickColor.Yellow()
	selectionBox.Adornee = nil
	selectionBox.Parent = player.PlayerGui

	selectionLasso = Instance.new("SelectionPartLasso")
	selectionLasso.Name = "Model Drag Lasso"
	selectionLasso.Humanoid = character.Humanoid
	selectionLasso.archivable = false
	selectionLasso.Visible = true
	selectionLasso.Parent = game.workspace
	selectionLasso.Color = BrickColor.Black()

	alreadyMoving = false
end

function onUnequippedLocal()
	Tool.TextureId = origTexture
	clearSelection()
	selectionBox:Remove()
	selectionLasso:Remove()
end


Tool.Equipped:connect(onEquippedLocal)
Tool.Unequipped:connect(onUnequippedLocal)