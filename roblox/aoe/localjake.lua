_G.AOE = {}
local SelectedUnits = {}
local WS = game:GetService("Workspace")

function OrderVectors(v1,v2)
	local minx,miny,minz,maxx,maxy,maxz
	if v1.x < v2.x then
		minx = v1.x
		maxx = v2.x
	else
		minx = v2.x
		maxx = v1.x
	end
	if v1.y < v2.y then
		miny = v1.y
		maxy = v2.y
	else
		miny = v2.y
		maxy = v1.y
	end
	if v1.z < v2.z then
		minz = v1.z
		maxz = v2.z
	else
		minz = v2.z
		maxz = v1.z
	end
	return Vector3.new(minx,miny,minz), Vector3.new(maxx,maxy,maxz)
end

function MathRound( num)
	local nodec = math.floor(num)
	if num-nodec<0.5 then
		return nodec
	else
		return math.ceil(num)
	end
end

print("LocalScript loaded!")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local ReceiveDataEvent = ReplicatedStorage:WaitForChild("ObjectDataEvent")
print("Found ObjectDataEvent")
local ply = game.Players.LocalPlayer
ReceiveDataEvent.OnClientEvent:Connect(function(data)
	local ReceivedData = data
	print("Received data!")

	if(ply.Team)then
		local food = data[ply.Team.Name].Resources.Food
		local wood = data[ply.Team.Name].Resources.Wood	
		--print("f:"..food.."w:"..wood)
		if food == nil and wood == nil then
			_G.AOE.Resources = "Food: 0 Wood: 0"
		elseif food == nil and wood ~= nil then
			_G.AOE.Resources = "Food: 0 Wood: " .. wood
		elseif food ~= nil and wood == nil then
			_G.AOE.Resources = "Food: ".. food .. " Wood: 0"
		elseif food ~= nil and wood ~= nil then
			_G.AOE.Resources = "Food: " .. food .. " Wood: " .. wood
		end
	end
	
	local tempdata = {}
	local function ConvertNumericalKeyToUserDataKey(t,ins_table)
		for k,v in pairs(t) do
			if type(v)=="table" then
				if v.Key then
					ins_table[v.Key] = {}
					ConvertNumericalKeyToUserDataKey(v,ins_table[v.Key])
				else
					ins_table[k] = {}
					ConvertNumericalKeyToUserDataKey(v,ins_table[k])
				end
			else
				ins_table[k] = v
			end
		end
	end	
	ConvertNumericalKeyToUserDataKey(ReceivedData,tempdata)
	TeamData = tempdata
end)
local ReceiveDataEvent2= ReplicatedStorage:WaitForChild("ObjectDataEvent2")

repeat wait() until TeamData --and ready
local ply = game.Players.LocalPlayer
local mouse = ply:GetMouse()

print("Objects received... past wait")

local hoverselection = Instance.new("SelectionBox")
hoverselection.Color3 = Color3.new(0.6,0.6,0,6)
hoverselection.Parent = ply.PlayerGui

local selection = Instance.new("SelectionBox")
selection.Color3 = Color3.new(0.6,0,0)
selection.Parent = ply.PlayerGui

local MouseButton1Down = false
local data
local frame,InitX,InitY
local starting,final
mouse.Move:Connect(function()
	local target = mouse.Target
	if not MouseButton1Down and target and target.Name:sub(1,ply.Team.Name:len())==ply.Team.Name then
		data = TeamData[ply.Team.Name].Units[target] or TeamData[ply.Team.Name].Buildings[target] -- detect if it's a valid game piece
		if data then -- if it is a valid game piece
			hoverselection.Adornee = target -- highlight it
		else
			hoverselection.Adornee = nil
		end
	else
		hoverselection.Adornee = nil
	end
	
	if frame then
		local PositionX = InitX
		local PositionY = InitY
	
		
		local SizeX,SizeY
		if mouse.X<PositionX then
			SizeX=PositionX-mouse.X
			PositionX=mouse.X
		else
			SizeX = mouse.X-PositionX
		end
		if mouse.Y<PositionY then
			SizeY=PositionY - mouse.Y
			PositionY=mouse.Y
		else
			SizeY = mouse.Y-PositionY
		end
		frame.Size = UDim2.new(0,SizeX,0,SizeY)
		frame.Position = UDim2.new(0,PositionX,0,PositionY)
		frame.Transparency = 0.7
		
		-- now the highlighting units crap
		SelectedUnits = {}
		local hitp = mouse.Hit.p
		local final = Vector3.new(hitp.x, 10, hitp.z)
		local min,max = OrderVectors(starting,final)

		local region = Region3.new(min,max)
			
		local parts = WS:FindPartsInRegion3(region)
		for k, part in pairs(parts)do
			if part.Name:sub(1,ply.Team.Name:len())==ply.Team.Name then
				
				data = TeamData[ply.Team.Name].Units[part] -- detect if it's a valid game piece
				if data then -- if it is a valid game piece
					
					local selectedUnit = Instance.new("SelectionBox")
					selectedUnit.Color3 = Color3.new(0.6,0,0)
					selectedUnit.Parent = ply.PlayerGui
					selectedUnit.Adornee = part
					table.insert(SelectedUnits, part)
				end
			end
		end
		
		-- Remove old selection boxes from units that are no longer selected
		for k,v in pairs(ply.PlayerGui:GetChildren()) do
			if v:IsA("SelectionBox") and v~=hoverselection and v~=selection then
				local good = false
				for i,c in pairs(SelectedUnits) do
					if v.Adornee==c then
						good = true
						break
					end
				end
				if not good then
					v:Destroy()
				end
			end
		end
		
	end
end)


mouse.Button1Down:Connect(function()
	MouseButton1Down = true
	if hoverselection.Adornee then
		if data.Food or data.Wood then
			if data.Food==nil and data.Wood==nil then
				selection.Adornee = hoverselection.Adornee
				_G.AOE.Text1 = "Food: 0"
				_G.AOE.Text2 = "Wood: 0"
			elseif data.Food==nil and data.Wood ~=nil then
				selection.Adornee = hoverselection.Adornee
				--print ("w "..data.Wood)
				_G.AOE.Text1 = "Food: 0"
				_G.AOE.Text2 = "Wood: " .. data.Wood
			elseif data.Food ~= nil and data.Wood == nil then
				selection.Adornee = hoverselection.Adornee
				--print("f "..data.Food)
				_G.AOE.Text1 = "Food: " .. data.Food
				_G.AOE.Text2 = "Wood: 0"
			elseif data.Food ~= nil and data.Wood ~= nil then
				selection.Adornee = hoverselection.Adornee
				--print("w "..data.Wood)
				--print("f "..data.Food)
				_G.AOE.Text1 = "Food: " .. data.Food
				_G.AOE.Text2 = "Wood: " .. data.Wood
			end
		else
			selection.Adornee = hoverselection.Adornee
			_G.AOE.Text1 = "Health: " .. (data.Health or "")
			_G.AOE.Text2 = "Attack: " .. (data.Attack or "")
			--_G.AOE.Text3 = "Range: " .. data.Range or ""
			--_G.AOE.Text4 = "IQ: ".. data.IQ or ""
		end
	else
		selection.Adornee = nil
		_G.AOE.Text1 = "N/A"
		_G.AOE.Text2 = "N/A"
		_G.AOE.Text3 = "N/A"
		_G.AOE.Text4 = "N/A"
		
		-- Remove all those selection things that we dont want to be selected any more.
		for k,v in pairs(ply.PlayerGui:GetChildren()) do
			if v:IsA("SelectionBox") and v~=selection and v~=hoverselection then
				v:Destroy()
			end
		end
		SelectedUnits = {}
		

		frame = Instance.new("Frame")
		frame.Parent = ply.PlayerGui.ScreenGui
		frame.Position = UDim2.new(0,mouse.X,0,mouse.Y)
		InitX = mouse.X
		InitY = mouse.Y
		local hitp = mouse.Hit.p
		starting = Vector3.new(hitp.x, -10, hitp.z)
	end
end)
mouse.Button1Up:Connect(function()
	MouseButton1Down = false
	if frame then
		frame:Destroy()
		frame = nil
	end
end)

mouse.Button2Down:Connect(function()
	if TeamData[ply.Team.Name].Buildings[selection.Adornee] then
		return -- Disallows buildings from being moved
	end
	if(mouse.Target.Name == "Bush")then
		_G.AOE.TextError = "Gathering from Bush!"
		return
	elseif(mouse.Target.Name == "Tree")then
		_G.AOE.TextError = "Gathering from Tree!"
		return
	elseif mouse.Target~= WS.Baseplate then
		--print("returned from mouse target detection")
		_G.AOE.TextError = "Already a unit at that position!"
		return
	end
	local numUnits = #SelectedUnits

	local v1 = Vector3.new(MathRound(mouse.Hit.p.x), MathRound(mouse.Hit.p.y), MathRound(mouse.Hit.p.z)) + Vector3.new(10, 1, 10)
	local v2 = Vector3.new(MathRound(mouse.Hit.p.x), MathRound(mouse.Hit.p.y), MathRound(mouse.Hit.p.z)) + Vector3.new(-10, 1, -10)
	local checkingRegion = Region3.new(v2, v1)
	
	local partsInRegion = WS:FindPartsInRegion3(checkingRegion)
		
	if SelectedUnits and #SelectedUnits>0 then
		for k, v in pairs(SelectedUnits)do
			if v and mouse.Target then
				for c, part in pairs(partsInRegion)do	
					local newPosition = Vector3.new(MathRound(mouse.Hit.p.x) + k, MathRound(mouse.Hit.p.y), MathRound(mouse.Hit.p.z))
					--print("table not sent yet")
					for TeamName, TeamTable in pairs(TeamData)do
						if TeamTable[TeamName].Units[part] and TeamTable[TeamName].Units[part].DesiredPosition ~= newPosition then
							ReceiveDataEvent:FireServer(newPosition, v)
							--print("table sent")
						end
					end
				end
			end
		end
	end
	if selection.Adornee and mouse.Target then
		local newPosition = Vector3.new(MathRound(mouse.Hit.p.x), MathRound(mouse.Hit.p.y), MathRound(mouse.Hit.p.z))
		for TeamName,TeamTable in pairs(TeamData) do
			for Unit,UnitTable in pairs(TeamTable.Units) do
				if Unit.Position == newPosition then
					print("returned from position conflict")
					return
				end
			end
		end
		--print("LocalScript.. Sending data: desiredPosition="..tostring(newPosition).. " target="..selection.Adornee:GetFullName())
		ReceiveDataEvent:FireServer(newPosition, selection.Adornee)
	end
end)










-- camera crap
repeat wait () until WS.CurrentCamera ~= nil
local camera = WS.CurrentCamera
camera.CameraType = "Scriptable"



-- keyboard input handling
local keys = {}
function onKeyPress(inputObject, gameProcessedEvent)
	keys[inputObject.KeyCode] = true
	
	if inputObject.KeyCode==Enum.KeyCode.V and hoverselection.Adornee  then
		print("V was pressed. ReceiveDataEvent2 triggered, sending adornee to server.")
		ReceiveDataEvent2:FireServer(selection.Adornee)
	elseif inputObject.KeyCode==Enum.KeyCode.I and camera.CFrame.p.y>25 then
		local movedistance = 1
		if keys[Enum.KeyCode.LeftShift] then
			movedistance = 5
		end
		camera.CFrame = camera.CFrame - Vector3.new(0,movedistance,0)
	elseif inputObject.KeyCode==Enum.KeyCode.O and camera.CFrame.p.y<75 then
		local movedistance = 1
		if keys[Enum.KeyCode.LeftShift] then
			movedistance = 5
		end
		camera.CFrame = camera.CFrame + Vector3.new(0,movedistance,0)
	end
end
game:GetService("UserInputService").InputBegan:Connect(onKeyPress)

function onKeyRelease(inputObject, gameProcessedEvent)
	keys[inputObject.KeyCode] = false
end
game:GetService("UserInputService").InputEnded:Connect(onKeyRelease)





-- more camera crap
local SetCameraPosition = ReplicatedStorage:WaitForChild("SetCameraPosition")
SetCameraPosition.OnClientEvent:Connect(function(pos,lookat)
	camera.CFrame = CFrame.new(pos, lookat)
	print("camera position updated, as commanded by server.")
end)


game:GetService('RunService').Stepped:connect(function()
	local movedistance = 1
	if keys[Enum.KeyCode.LeftShift] then
		movedistance = 5
	end
	if MouseButton1Down then
		return
	end
	if keys[Enum.KeyCode.W] and camera.CFrame.p.x<WS.Baseplate.Size.x/2 then
		camera.CFrame = camera.CFrame + Vector3.new(movedistance,0,0)
	elseif keys[Enum.KeyCode.S] and camera.CFrame.p.x>-WS.Baseplate.Size.x/2 then
		camera.CFrame = camera.CFrame - Vector3.new(movedistance,0,0)
	end
	if keys[Enum.KeyCode.D] and camera.CFrame.p.z<WS.Baseplate.Size.z/2 then
		camera.CFrame = camera.CFrame + Vector3.new(0,0,movedistance)
	elseif keys[Enum.KeyCode.A] and camera.CFrame.p.z>-WS.Baseplate.Size.z/2 then
		camera.CFrame = camera.CFrame - Vector3.new(0,0,movedistance)
	end
end)

mouse.WheelBackward:Connect(function()
	if MouseButton1Down or camera.CFrame.p.y>75 then
		return
	end
	local movedistance = 1
	if keys[Enum.KeyCode.LeftShift] then
		movedistance = 5
	end
	camera.CFrame = camera.CFrame + Vector3.new(0,movedistance,0)
end)

mouse.WheelForward:Connect(function()
	if MouseButton1Down or camera.CFrame.p.y<25 then
		return
	end
	local movedistance = 1
	if keys[Enum.KeyCode.LeftShift] then
		movedistance = 5
	end
	camera.CFrame = camera.CFrame - Vector3.new(0,movedistance,0)
end)
