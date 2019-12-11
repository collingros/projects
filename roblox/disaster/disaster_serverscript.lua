local message = Instance.new("Message")
local timeTop = Instance.new("Hint")
timeTop.Parent = game.Workspace

function Reset() -- destroys all props and kills all players, returns true when reset is over
	local str = "The world is being reset..."
	MakeMsg(str, 2)
	for k,v in pairs(game.Workspace:GetChildren()) do
		if v.ClassName=="Part" and v.Name~="Baseplate"then-- deletes every object called "Part"
			v:Destroy()
		end
	end
	for k, f in pairs(game.ServerStorage:GetChildren())do -- moves tools back into starter pack after disaster
		if (f.ClassName == "Tool")then
			f.Parent = game.StarterPack
		elseif (f.Name == "BuildBlocks")then
			f.Parent = game.Workspace
		end
	end
	for k,ply in pairs(game.Players:GetPlayers()) do -- kills players
		ply.Character.Humanoid.Health = 0
	end
end

function Build(seconds) -- displays build, unanchors all objects
	local str = "Building Period: You have 5 minutes to build a structure in order to survive the disaster!"
	MakeMsg(str, 5)
	TeleportPlayers()
	local currentTime = seconds
	while (currentTime >= 0)do
		timeTop.Text = currentTime
		wait(1)
		currentTime = currentTime - 1
	end
	

	--[[for k,v in pairs(game.Workspace:GetChildren())do
		if (v.ClassName == "Part" and (v.Name ~= "Spawn" and v.Name ~= "Baseplate"))then
			v.Anchored = false
		end
	end--]]
end

function PickDisaster()
	print("pick disaster called") -- picks a random disaster out of the list of disasters, returns the disaster picked
	local disaster
	local MeteorShower = "MeteorShower"
	local Warzone = "Warzone"
	local Earthquake = "Earthquake"
	local Apocalypse = "Apocalypse"
	local Avalanche = "Avalanche"
	local LavaFlood = "LavaFlood"
-- Warzone, Earthquake, Apocalypse, LavaFlood
	local disasterList = {MeteorShower, Avalanche}
	local pickedDisasterNumber = math.random(#disasterList)
	disaster = disasterList[pickedDisasterNumber]
	return LavaFlood
end

-- DISASTER FUNCTIONS
function MeteorShower(seconds) -- shoots meteors from the sky to damage props
	local str = "The disaster is: METEOR SHOWER!"
	MakeMsg(str, 2)
	local dst = "MeteorShower"	
	
	local currentTime = seconds
	while (currentTime >= 0)do
		for k, v in pairs (game.Players:GetPlayers())do
			local playerpos = v.Character.Torso.Position -- sets up meteor position and properties
			local meteor = Instance.new ("Part")
			meteor.Shape = "Ball"
			meteor.Parent = game.Workspace
			meteor.Size = Vector3.new(10, 10, 10)
			meteor.Name = "Meteor"
			meteor.BrickColor = BrickColor.new("Bright orange")
			local fire = Instance.new("Fire")
			fire.Parent = meteor
			meteor.TopSurface = "Smooth"
			meteor.Touched:connect(function(otherPart)
					killOnTouch(otherPart, dst)
					meteor:Destroy()
			end)
			print("meteor touched called")
			timeTop.Text = currentTime
			math.randomseed(os.time())
			wait(1)
			print("wait called")
			currentTime = currentTime - 1
			
			local decider = math.random(1000) -- the reason for this section is to make meteors spawn in random vertices of a square above each player, also 1000 because more variation
			if (decider <= 250)then
				meteor.Position = playerpos + Vector3.new (math.random(10),480, 0)
			elseif (decider > 250 and decider < 500) then
				meteor.Position = playerpos + Vector3.new (-math.random(10), 480, 0)
			elseif (decider > 500 and decider < 750) then
				meteor.Position = playerpos + Vector3.new (0, 480, math.random(10))
			elseif (decider >= 750) then
				meteor.Position = playerpos + Vector3.new (0, 480, -math.random(10))
			end
			
			--[[meteor.Touched:connect(function(otherPart) -- if meteor is touched killOnTouch() called
				killOnTouch(otherPart)
				meteor:Destroy() -- Thinking about creating  a script in every meteor with this in case wait interferes with it, need to test it
			end)--]]
		end
	end
end

function killOnTouch(part, dst)
	if part.Parent.ClassName == "Model" then
		local ply = game.Players:GetPlayerFromCharacter(part.Parent)
		if ply and ply~=nil then
			ply.Character.Humanoid.Health = 0
		end
	end
	if (part ~= game.Workspace.Spawn and part ~= game.Workspace.Baseplate and part.Name ~= "Ramp") then
		part.Anchored = false 
	end
	
	if (dst == "MeteorShower")then
		game.Soundscape.Explosion:Play()
	end
end

function LavaFlood(seconds) -- spawns lava around players and slowly rises, players die on touch
	local str = "The disaster is: LAVA FLOOD!"
	MakeMsg(str, 2)
	local lava = Instance.new("Part")
	lava.Parent = game.Workspace
	lava.Size = Vector3.new(500, 1, 500)
	lava.BrickColor = BrickColor.new(106)
	lava.CFrame = CFrame.new(0, 0, 0)
	lava.Material = "Sand"
	lava.Anchored = true
	lava.Locked = true
	local num = 0
	lava.CanCollide = false
	print("before currenttime")
	local currentTime = seconds
	lava.Touched:connect(function(otherPart)
		killOnTouch(otherPart, nil)
	end)
	while(currentTime >= 0)do
		print("looping")
		local pos = lava.Position
		local size = lava.Size
		num = num + 1
		lava.Position = pos + Vector3.new(0, num, 0)
		lava.Size = size + Vector3.new(0, num, 0)

		timeTop.Text = currentTime
		wait(1)
		currentTime = currentTime - 1
	end
end
function WorldEater() -- spawns a plate at the top of the map and makes props float up towards it as well as players, players die when they hit. plays cool sound
	
end
function Warzone() -- spawns soldier models and fires rockets at props
	message.Text = "The disaster is: WARZONE!"
	message.Parent = game.Workspace
	wait(2)
	message.Parent = nil
end

function Earthquake() -- shake's player's camera and damages props
	message.Text = "The disaster is: EARTHQUAKE!"
	message.Parent = game.Workspace
	wait(2)
	message.Parent = nil
end

function Apocalypse()
	message.Text = "The disaster is: APOCALYPSE!"
	message.Parent = game.Workspace
	wait(2)
	message.Parent = nil

	
	
end



function Avalanche(seconds)
	local str = "The disaster is: AVALANCHE!"
	MakeMsg(str, 2)
	
	local ramp = Instance.new("Part")
	ramp.Parent = game.Workspace
	ramp.BrickColor = BrickColor.new(26)
	ramp.Name = "Ramp"
	ramp.Size = Vector3.new(300, 1, 500)
	ramp.Rotation = Vector3.new(0,0,-30)
	ramp.Position = Vector3.new(-310, 50, 0)
	ramp.Material = "Ice" -- ice material to ramp for less friction
	ramp.Anchored = true
	ramp.Locked = true
	
	local currentTime = seconds
	while (currentTime >= 0)do
		local ice = Instance.new("Part")
		ice.BrickColor = BrickColor.new(1013)
		ice.Transparency = 0.5
		ice.Size = Vector3.new(25, 20, 30)
		ice.Anchored = false
		ice.Locked = true
		ice.Material = "Ice"
		ice.Touched:connect(function(otherPart) -- may need to be in another script inside ice as the wait may interfere (4/21/2017)
				killOnTouch(otherPart)
		end)
		print("ice touched called")
		timeTop.Text = currentTime
		math.randomseed(os.time())
		wait(1)
		print("wait called")
		currentTime = currentTime - 1
		
		local num = math.random(-200,200)
		ice.Position = Vector3.new(-400, 290, num)
		ice.Parent = game.Workspace
		
	end
	str = "Congratulations to all survivors!"
	MakeMsg(str, 5)
end



function StartDisaster(disaster, seconds)
	print ("start disaster called")
	for k,d in pairs(game.Players:GetChildren())do
			d.Character.Humanoid:UnequipTools()
		for k,e in pairs(d.Backpack:GetChildren())do
			e:Destroy()
		end
	end
	
	for k, f in pairs(game.StarterPack:GetChildren())do
			f.Parent = game.ServerStorage
	end
	
	game.Workspace.BuildBlocks.Parent = game.ServerStorage -- moves buildblocks out of workspace

	
	if (disaster == "MeteorShower") then 
		MeteorShower(seconds)
	elseif (disaster == "Warzone") then 
		Warzone()
	elseif (disaster == "Earthquake") then
		Earthquake()
	elseif (disaster == "Apocalypse") then
		Apocalypse()
	elseif (disaster == "Avalanche") then
		Avalanche(seconds)
	elseif (disaster == "LavaFlood")then
		LavaFlood(seconds)
	end
end

function TeleportPlayers()
	for k, v in pairs (game.Players:GetPlayers())do
		if v.Character then
			local position = v.Character.Torso.Position
			v.Character:MoveTo(position - Vector3.new(0, 500, 1))
		end
	end
end

function MakeMsg(msg, sec)
	message.Text = msg
	message.Parent = game.Workspace
	wait(sec)
	message.Parent = nil
end
-- MAIN FUNCTION

while true do
	Build(6)
	StartDisaster(PickDisaster(), 30)
	Reset()
	wait(2)
end
-- END OF MAIN FUNCTION






 