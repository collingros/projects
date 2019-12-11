Tool = script.Parent
Tool.Enabled = true

function onActivated()

	if not Tool.Enabled then
		return
	end

	Tool.Enabled = false

	local character = Tool.Parent;
	local humanoid = character.Humanoid
	if humanoid == nil then
		print("Humanoid not found")
		return 
	end

	Tool.Enabled = true
end


function onEquipped()
end


script.Parent.Activated:connect(onActivated)
script.Parent.Equipped:connect(onEquipped)

