local TeamData = {}
local TakenSpots = {}
local Nature = {}


local WS = game:GetService("Workspace")
local RS = game:GetService("ReplicatedStorage")
local GameRunning = false


-- Remote Events
local SetCameraPosition = Instance.new("RemoteEvent", RS)
SetCameraPosition.Name = "SetCameraPosition"

local SendDataEvent = Instance.new("RemoteEvent", RS)
SendDataEvent.Name = "ObjectDataEvent"

local SendDataEvent2 = Instance.new("RemoteEvent", RS)
SendDataEvent2.Name = "ObjectDataEvent2"




function MathRound(num)
	local nodec = math.floor(num)
	if num-nodec<0.5 then
		return nodec
	else
		return math.ceil(num)
	end
end

function GenerateTerrain()
	local m = Instance.new("Model")
	for k = -173, 176, 4 do
		for x = -173, 176, 4 do
			local currentDot = Vector3.new(k, 2, x)
			local mag = (currentDot - Vector3.new(0, 1, 0)).magnitude
			if (mag > 150 and mag < 151)then
				
				local bush = Instance.new("Part")
				bush.Name = "Bush"
				bush.Size = Vector3.new(3,1,3)
				bush.BrickColor = BrickColor.new(304)
				bush.Anchored = true
				bush.CFrame = CFrame.new(k, 1, x)
				bush.Parent = m
			
				Nature[bush] = {Class = "Bush", Health = 5, Food = 100, Spots = {}, Object = bush}
				table.insert(Nature[bush].Spots, {Position=bush.Position+Vector3.new(-1,0,2)})
				table.insert(Nature[bush].Spots, {Position=bush.Position+Vector3.new(0,0,2)})
				table.insert(Nature[bush].Spots, {Position=bush.Position+Vector3.new(1,0,2)})
				table.insert(Nature[bush].Spots, {Position=bush.Position+Vector3.new(2,0,1)})
				table.insert(Nature[bush].Spots, {Position=bush.Position+Vector3.new(2,0,0)})
				table.insert(Nature[bush].Spots, {Position=bush.Position+Vector3.new(2,0,-1)})
				table.insert(Nature[bush].Spots, {Position=bush.Position+Vector3.new(1,0,-2)})
				table.insert(Nature[bush].Spots, {Position=bush.Position+Vector3.new(0,0,-2)})
				table.insert(Nature[bush].Spots, {Position=bush.Position+Vector3.new(-1,0,2)})
				table.insert(Nature[bush].Spots, {Position=bush.Position+Vector3.new(-2,0,-1)})
				table.insert(Nature[bush].Spots, {Position=bush.Position+Vector3.new(-2,0,0)})
				table.insert(Nature[bush].Spots, {Position=bush.Position+Vector3.new(-2,0,1)})

			end
			if (mag < 100) then
				local tree = Instance.new("Part")
				tree.Name = "Tree"
				tree.Size = Vector3.new(1, 3, 1)
				tree.BrickColor = BrickColor.new(216)
				tree.Anchored = true
				tree.CFrame = CFrame.new(k, 2, x)
				tree.Parent = m
				Nature[tree] = {Class="Tree", Health = 5, Wood = 100, Spots = {}, Object = tree}
				table.insert(Nature[tree].Spots, {Position=tree.Position+Vector3.new(1,0,0)})
				table.insert(Nature[tree].Spots, {Position=tree.Position+Vector3.new(-1,0,0)})
				table.insert(Nature[tree].Spots, {Position=tree.Position+Vector3.new(0,0,-1)})
				table.insert(Nature[tree].Spots, {Position=tree.Position+Vector3.new(0,0,1)})
		
			end
		end
	end
	m.Parent = WS
	MAP = m
end

function GatherResources(villager, resource)
	local CollectResource = {
		Bush = function()
			if(resource.Food > 0)then
				resource.Food = resource.Food - 1
				villager.Food = villager.Food + 1
				--print(string.format("Villager has %s food, resource has %s food remaining.",villager.Food,resource.Food))
			else
				resource.Object:Destroy()
				Nature[resource] = nil
				villager.GatherPartTable = nil
			end
		end,
		Tree = function()
			if(resource.Wood > 0)then
				resource.Wood = resource.Wood - 1
				villager.Wood = villager.Wood + 1
				--print(string.format("Villager has %s wood, resource has %s wood remaining.",villager.Wood,resource.Wood))
			else
				resource.Object:Destroy()
				Nature[resource] = nil
				villager.GatherPartTable = nil
			end
		end
	}
	CollectResource[resource.Class]()
end


function DepositResources(TeamName, Villager, TownCenter)
	--TownCenter.Food = TownCenter.Food + Villager.Food
	TeamData[TeamName].Resources.Food = TeamData[TeamName].Resources.Food + Villager.Food
	Villager.Food = 0
	
	--TownCenter.Wood = TownCenter.Wood + Villager.Wood
	TeamData[TeamName].Resources.Wood = TeamData[TeamName].Resources.Wood + Villager.Wood
	Villager.Wood = 0
	print(TeamName .. " deposited!")
	--print("TC Food: " .. TownCenter.Food .. "TC Wood: " .. TownCenter.Wood)
end

function CreateTownCenter(ply,pos)
	local TC = Instance.new("Part", MAP)
	TC.Size = Vector3.new(5,1,5)
	TC.Position = pos
	TC.BrickColor = ply.TeamColor
	TC.Name = ply.Team.Name .. "TC"
	TC.Anchored = true
	TeamData[ply.Team.Name].Buildings[TC] = {Class="TownCenter",Health=500, Food = TeamData[ply.Team.Name].Resources.Food, Wood = TeamData[ply.Team.Name].Resources.Wood, Spots = {}}
	
	-- all spots around tc
	
	table.insert(TeamData[ply.Team.Name].Buildings[TC].Spots, {Position=TC.Position+Vector3.new(3,0,-3)})
	table.insert(TeamData[ply.Team.Name].Buildings[TC].Spots, {Position=TC.Position+Vector3.new(3,0,-2)})
	table.insert(TeamData[ply.Team.Name].Buildings[TC].Spots, {Position=TC.Position+Vector3.new(3,0,-1)})
	table.insert(TeamData[ply.Team.Name].Buildings[TC].Spots, {Position=TC.Position+Vector3.new(3,0,0)})
	table.insert(TeamData[ply.Team.Name].Buildings[TC].Spots, {Position=TC.Position+Vector3.new(3,0,1)})
	table.insert(TeamData[ply.Team.Name].Buildings[TC].Spots, {Position=TC.Position+Vector3.new(3,0,2)})
	table.insert(TeamData[ply.Team.Name].Buildings[TC].Spots, {Position=TC.Position+Vector3.new(3,0,3)})
	table.insert(TeamData[ply.Team.Name].Buildings[TC].Spots, {Position=TC.Position+Vector3.new(-3,0,-3)})
	table.insert(TeamData[ply.Team.Name].Buildings[TC].Spots, {Position=TC.Position+Vector3.new(-3,0,-2)})
	table.insert(TeamData[ply.Team.Name].Buildings[TC].Spots, {Position=TC.Position+Vector3.new(-3,0,-1)})
	table.insert(TeamData[ply.Team.Name].Buildings[TC].Spots, {Position=TC.Position+Vector3.new(-3,0,0)})
	table.insert(TeamData[ply.Team.Name].Buildings[TC].Spots, {Position=TC.Position+Vector3.new(-3,0,1)})
	table.insert(TeamData[ply.Team.Name].Buildings[TC].Spots, {Position=TC.Position+Vector3.new(-3,0,2)})
	table.insert(TeamData[ply.Team.Name].Buildings[TC].Spots, {Position=TC.Position+Vector3.new(-3,0,3)})
	table.insert(TeamData[ply.Team.Name].Buildings[TC].Spots, {Position=TC.Position+Vector3.new(-2,0,3)})
	table.insert(TeamData[ply.Team.Name].Buildings[TC].Spots, {Position=TC.Position+Vector3.new(-1,0,3)})
	table.insert(TeamData[ply.Team.Name].Buildings[TC].Spots, {Position=TC.Position+Vector3.new(0,0,3)})
	table.insert(TeamData[ply.Team.Name].Buildings[TC].Spots, {Position=TC.Position+Vector3.new(1,0,3)})
	table.insert(TeamData[ply.Team.Name].Buildings[TC].Spots, {Position=TC.Position+Vector3.new(2,0,3)})
	table.insert(TeamData[ply.Team.Name].Buildings[TC].Spots, {Position=TC.Position+Vector3.new(-2,0,-3)})
	table.insert(TeamData[ply.Team.Name].Buildings[TC].Spots, {Position=TC.Position+Vector3.new(-1,0,-3)})
	table.insert(TeamData[ply.Team.Name].Buildings[TC].Spots, {Position=TC.Position+Vector3.new(0,0,-3)})
	table.insert(TeamData[ply.Team.Name].Buildings[TC].Spots, {Position=TC.Position+Vector3.new(1,0,-3)})
	table.insert(TeamData[ply.Team.Name].Buildings[TC].Spots, {Position=TC.Position+Vector3.new(2,0,-3)})
	
end

--creation

function CreateVillager(ply,pos)
	local V = Instance.new("Part", MAP)
	V.Size = Vector3.new(1,1,1)
	V.Position = pos
	V.BrickColor = ply.TeamColor
	V.Name = ply.Team.Name .. "Villager"
	V.Anchored = true
	TeamData[ply.Team.Name].Units[V] = {Class="Villager",Health = 10, Wood = 0, Food=0,Attack = 1, LastGather = 0}
end


function StartNewGame() -- autism
	math.randomseed(tick())
	_G.playerWon = false
	for k,v in pairs(game.Players:GetPlayers()) do
		TeamData[v.Team.Name] = {}
		TeamData[v.Team.Name].Units = {}
		TeamData[v.Team.Name].Buildings = {}
		TeamData[v.Team.Name].Resources = {Food = 100, Wood = 100}
		local pos1 = Vector3.new(0, 1, -150) -- blue
		local pos2 = Vector3.new(150, 1, 0) -- red
		local pos3 = Vector3.new(0, 1, 150) -- yellow
		local pos4 = Vector3.new(-150, 1, 0) -- green
		GenerateTerrain()
		if v.Team.Name == "Blue" then
			SetCameraPosition:FireClient(v,pos1+Vector3.new(0,25,0),pos1)
			CreateTownCenter(v, pos1)
			for i = 1, 3 do
				CreateVillager(v, pos1 + Vector3.new(math.random(-10, 10), 0, math.random(-10, 10)))
			end
		elseif v.Team.Name == "Red" then
			SetCameraPosition:FireClient(v,pos2+Vector3.new(0,25,0),pos2)
			CreateTownCenter(v, pos2)
			for i = 1, 3 do
				CreateVillager(v, pos2 + Vector3.new(math.random(-10, 10), 0, math.random(-10, 10)))
			end
		elseif v.Team.Name == "Yellow" then
			SetCameraPosition:FireClient(v,pos3+Vector3.new(0,25,0),pos3)
			CreateTownCenter(v, pos3)
			for i = 1, 3 do
				CreateVillager(v, pos3 + Vector3.new(math.random(-10, 10), 0, math.random(-10, 10)))
			end
		elseif v.Team.Name == "Green" then
			SetCameraPosition:FireClient(v,pos4+Vector3.new(0,25,0),pos4)
			CreateTownCenter(v, pos4)
			for i = 1, 3 do
				CreateVillager(v, pos4 + Vector3.new(math.random(-10, 10), 0, math.random(-10, 10)))
			end
		end
	end
	GameRunning = true
end


local count = 0
game.Players.PlayerAdded:Connect(function(ply)
	-- StarterGui is only automatically cloned when a character is added. In this game, the character is never added.
	for k,v in pairs(game:GetService("StarterGui"):GetChildren()) do
		v:Clone().Parent = ply.PlayerGui
	end
	
	StartNewGame()
	UpdateTable()
end)


function UpdateTable()
	local tempdata = {}
	-- You can't have userdata as a key when you send data to the client, so this converts tables to have non-userdata keys before sent.
	local function ConvertUserDataKeyToNumericalKey(t,ins_table)
		for k,v in pairs(t) do
			if type(k)=="userdata" then
				local t = v
				t.Key = k
				table.insert(ins_table,t)
				local newkey = #ins_table
				if type(v)=="table" then
					ins_table[newkey] = {}
					ConvertUserDataKeyToNumericalKey(v,ins_table[newkey])
				end
			elseif type(v)=="table" then
				ins_table[k] = {}
				ConvertUserDataKeyToNumericalKey(v,ins_table[k])
			else
				ins_table[k] = v
			end
		end
	end	
	ConvertUserDataKeyToNumericalKey(TeamData,tempdata)
	SendDataEvent:FireAllClients(tempdata)
		
end


local laststep = 0
game:GetService('RunService').Stepped:connect(function(gametime,steptime)
	if not GameRunning then return end
	if gametime-laststep >= 0.125 then
		laststep = gametime
		UpdateTable()
		
		
		for TeamName,TeamTable in pairs(TeamData) do
			for Unit,UnitTable in pairs(TeamTable.Units) do
				0if UnitTable.DesiredPosition then
					if UnitTable.DesiredToMoveByPlayer then
						UnitTable.DesiredToMoveByPlayer = nil
						if UnitTable.GatherPartTable and UnitTable.Spot then
							UnitTable.Spot.TakenBy = nil
						end
						UnitTable.GatherPartTable = nil
						UnitTable.Spot = nil
					end

					if (UnitTable.DesiredPosition.X < Unit.Position.X)then 
						Unit.Position = Unit.Position - Vector3.new(1, 0, 0)
					end
					if (UnitTable.DesiredPosition.X > Unit.Position.X)then 
						Unit.Position = Unit.Position + Vector3.new(1, 0, 0)
					end
					if (UnitTable.DesiredPosition.Y < Unit.Position.Y)then 
						local newpos =  Unit.Position - Vector3.new(0, 1, 0)
						Unit.Position = Vector3.new(MathRound(newpos.x),MathRound(newpos.y),MathRound(newpos.z))
					end
					if (UnitTable.DesiredPosition.Y > Unit.Position.Y)then 
						local newpos = Unit.Position + Vector3.new(0, 1, 0)
						Unit.Position = Vector3.new(MathRound(newpos.x),MathRound(newpos.y),MathRound(newpos.z))
					end
					if (UnitTable.DesiredPosition.Z < Unit.Position.Z)then 
						Unit.Position = Unit.Position - Vector3.new(0, 0, 1)
					end
					if (UnitTable.DesiredPosition.Z > Unit.Position.Z)then 
						Unit.Position = Unit.Position + Vector3.new(0, 0, 1)
					end
				
					
					if (UnitTable.DesiredPosition == Unit.Position)then
						print("At position!")
						UnitTable.DesiredPosition = nil
						if UnitTable.Class=="Villager" then
							print("Is Villager!")
							
							-- If the villager has resources, and they are at a spot on a towncenter then...
							if (UnitTable.Wood>0 or UnitTable.Food>0) and UnitTable.NearestTownCenterTable and UnitTable.Spot  and UnitTable.NearestTownCenterTable.Class=="TownCenter" then
								--print("we have resources to deposit")							

								if(Unit.Position == UnitTable.Spot.Position)then
									print("unit position == spot position, resources deposited")
									DepositResources(TeamName, UnitTable, UnitTable.NearestTownCenterTable)
									UnitTable.NearestTownCenterTable = nil
									UnitTable.Spot.TakenBy = nil
									if UnitTable.GatherPartTable then
											-- Get nearest spot on previous resource
											local dist = math.huge
											for k,Spot in pairs(UnitTable.GatherPartTable.Spots) do -- cant view gatherpart as a table, its a part
												if not Spot.TakenBy then
													local tempdist = (Unit.Position-Spot.Position).magnitude
													if tempdist<dist then
														dist=tempdist
														UnitTable.Spot = Spot
														Spot.TakenBy = Unit
														UnitTable.DesiredPosition = Spot.Position
													end
												end
											end
										end
									end
							elseif not UnitTable.GatherPartTable then
								print("we don't have a gatherpart, lets get one!")
								-- find a new GatherPart that is near us
								local max = Unit.Position + Vector3.new(5, 3, 5)
								local min = Unit.Position + Vector3.new(-5, -2, -5)
								local region = Region3.new(min, max)
								local parts = WS:FindPartsInRegion3(region)
											
								local dist = math.huge
								local NearestAvailableSpot
								
								if #parts>1 then -- >1 because the baseplate will always be one of the results
									
									-- find nearest resource
									for x, resource in pairs(parts)do
										if (Nature[resource])then
											local tempdist = (Unit.Position-resource.Position).magnitude
											if tempdist<dist then
												dist=tempdist
												UnitTable.GatherPartTable = Nature[resource]
												UnitTable.LastResourcePosition = resource.Position
											end
										end
									end
											
									-- find nearest spot at that resource
									if UnitTable.GatherPartTable then
										for k,Spot in pairs(UnitTable.GatherPartTable.Spots) do
											if not Spot.TakenBy then
												local tempdist = (Unit.Position-Spot.Position).magnitude
												if tempdist<dist then
													dist=tempdist
													UnitTable.Spot = Spot
													UnitTable.Job = "ResourceCollector"
													UnitTable.DesiredPosition = Spot.Position
													Spot.TakenBy = Unit
												end
											end
										end
									else
										print("No resources in range. Standing by.")
									end
								end			

							end
						end
					end
				
				else -- desired position doesn't exist. Part must be stationary
					-- Go to the existing gatherpart
					if UnitTable.Job == "ResourceCollector" then
						--print("Job is a ResourceCollector")
						if not UnitTable.GatherPartTable then
							--print("We don't have a gather part.")
						end
						if UnitTable.LastResourcePosition then
							--print("We have a last resource position.")
						end
						if not UnitTable.GatherPartTable and UnitTable.LastResourcePosition then
							print("Previously had a gather part that has since been removed, searching for a new one.")
							local max = Unit.Position + Vector3.new(25, 3, 25)
							local min = Unit.Position + Vector3.new(-25, -2, -25)
							local region = Region3.new(min, max)
							local parts = WS:FindPartsInRegion3(region)
							local continue = true
							for k,v in pairs(parts) do
								if Nature[v] then
									continue = false
									print("Found a new resource, setting all villagers at current resource to it.")
									for i,c in pairs(TeamTable.Units) do
										if c.LastResourcePosition==UnitTable.LastResourcePosition then
											c.GatherPartTable=Nature[v]
											-- Get nearest spot on previous resource
											local dist = math.huge
											for k,Spot in pairs(Nature[v].Spots) do -- cant view gatherpart as a table, its a part
												if not Spot.TakenBy then
													local tempdist = (i.Position-Spot.Position).magnitude
													if tempdist<dist then
														dist=tempdist
														c.Spot = Spot
														Spot.TakenBy = Unit
														c.DesiredPosition = Spot.Position
													end
												end
											end
										end
									end
								return -- all our parts will go to the new resource on the next Step around.
								end
							end
							
							if continue and TakenSpots[UnitTable.LastResourcePosition] then
								local OpenSpots = TakenSpots[UnitTable.LastResourcePosition]
								local remaining_open_spots = {}
								local MySpot
								local SpotCount = 0
								for k,v in pairs(OpenSpots) do
									if not MySpot then
										MySpot = v
									else
										SpotCount = SpotCount + 1
										table.insert(remaining_open_spots,v)
									end
								end
								if SpotCount==0 then
									OpenSpots = nil
									UnitTable.DesiredPosition = nil
								else
									OpenSpots = remaining_open_spots
									UnitTable.DesiredPosition = MySpot
								end
							else
								local backup_positions = {}
								local backup_positions_available = {}
								for i=-3,3 do
									for j=-3,3 do
										table.insert(backup_positions,UnitTable.LastResourcePosition+Vector3.new(i,0,j))
										table.insert(backup_positions_available,UnitTable.LastResourcePosition+Vector3.new(i,0,j))
									end
								end
	
								local min = UnitTable.LastResourceSpotPosition + Vector3.new(-5,-2,-5)
								local max = UnitTable.LastResourceSpotPosition + Vector3.new(5,3,5)
								local region = Region3.new(min,max)
								local parts = WS:FindPartsInRegion3(region)
								if parts>1 then -- >1 because the baseplate will always be one of the results
									local MySpot
									for i,c in pairs(backup_positions) do
										
										for k,v in pairs(parts) do
											if v.Position==c then
												table.remove(backup_positions_available,i)
												break
											elseif not MySpot then
												MySpot = c 
												table.remove(backup_positions_available,i)
											end
										end
									end
									TakenSpots[UnitTable.LastResourceSpotPosition] = backup_positions_available
								end
							end
						elseif UnitTable.GatherPartTable and (gametime - UnitTable.LastGather > 1)then
							local ResourceTable = Nature[UnitTable.GatherPartTable]
							if UnitTable.GatherPartTable then
								GatherResources(UnitTable, UnitTable.GatherPartTable)
							end
							UnitTable.LastGather = gametime
							
							if UnitTable.Wood == 10 or UnitTable.Food == 10 then
								
								-- Remove ourselves from this resources spot. Make it available for another villager
								UnitTable.Spot.TakenBy = nil
								
								print("we have max resource, lets find a TC nearby...")
								-- find nearest towncenter
								local dist = math.huge
								for Building,BuildingTable in pairs(TeamData[TeamName].Buildings) do
									if BuildingTable.Class == "TownCenter" then
										local tempdist = (Unit.Position-Building.Position).magnitude
										if tempdist<dist then
											dist = tempdist
											UnitTable.NearestTownCenterTable = BuildingTable
										end
									end
								end
								-- Find nearest spot at that towncenter
								dist = math.huge
								local NearestAvailableSpot
								for k,Spot in pairs(UnitTable.NearestTownCenterTable.Spots) do
									if not Spot.TakenBy then
										local tempdist = (Unit.Position-Spot.Position).magnitude
										if tempdist<dist then
											dist=tempdist
											UnitTable.Spot = Spot
											Spot.TakenBy = Unit
											UnitTable.DesiredPosition = Spot.Position
										end
									end
								end
								print("TC found, Spot found")
							end -- if max food/wood reached
						end -- gathering food/wood per second
					end -- If our job is a ResourceCollector
				end -- if desired position exists
			end -- for units
		end -- for teams
	end -- Step increment
end) -- Stepped

function CheckIfOpen(player, newPosition)
	local desiredPosition
	for Unit, UnitTable in pairs(TeamData[player.Team.Name].Units) do
		desiredPosition = UnitTable.DesiredPosition
		if desiredPosition ~= newPosition then
			return newPosition
		else
			return newPosition + Vector3.new(1, 0, 0)
		end
	end
end

SendDataEvent.OnServerEvent:Connect(function(player, newPosition, target)
	for Unit,UnitTable in pairs(TeamData[player.Team.Name].Units) do
		--[[local backup_positions = {}
		local backup_positions_available = {}
		for i=-3,3 do
			for j=-3,3 do
				table.insert(backup_positions,UnitTable.LastResourcePosition+Vector3.new(i,0,j))
				table.insert(backup_positions_available,UnitTable.LastResourcePosition+Vector3.new(i,0,j))
			end
		end
	]]
		if Unit == target then
			TeamData[player.Team.Name].Units[Unit].DesiredPosition = CheckIfOpen(player, newPosition)
			TeamData[player.Team.Name].Units[Unit].DesiredToMoveByPlayer = true
		end
	end
end)

SendDataEvent2.OnServerEvent:Connect(function(player, building)
	--print("SendDataEvent2 script called")
	for Building, BuildingTable in pairs (TeamData[player.Team.Name].Buildings)do
		--print("for")
		if BuildingTable.Class == "TownCenter"then
			--print("first if")
			if (building == Building) and TeamData[player.Team.Name].Resources.Food >= 50 then
				--print("second if")
				--TeamData[player.Team.Name].Buildings[Building].Food = TeamData[player.Team.Name].Buildings[Building].Food - 50
				TeamData[player.Team.Name].Resources.Food = TeamData[player.Team.Name].Resources.Food - 50
				CreateVillager(player, (Building.Position + Vector3.new(math.random(-10, 10), 0, math.random(-10, 10))))
				UpdateTable()
				break
			end
		end
	end
end)
