--!strict
-- House-rule scan (read-only). Finds visible primitive Parts, meshes that may not be
-- the owner's own, world geometry players can walk through, and other house-rule debt.
--
-- Run in EDIT mode only, never in a live server:
--   * Studio command bar: paste the whole file, or
--   * Studio MCP: execute_luau with datamodel_type = "Edit" and this file's contents.
-- It prints a grouped, capped report and changes nothing.
-- Unexecuted sketch: reviewed by reading, never run in Studio. Test it on a copy of the place first.
-- Rules it checks and how to read the output: references/checklists.md, Gate 4.

local MarketplaceService = game:GetService("MarketplaceService")

local MAX_ROWS = 25 -- areas printed
local CREATOR_CHECKS = 30 -- most-used MeshIds to look up; 0 skips the lookup
local CHECK_PAUSE = 0.5 -- seconds between lookups; GetProductInfoAsync is rate-limited
local PRIM, NOCOL, SHADOW = 1, 2, 3

local roots: { Instance } = { workspace, game:GetService("ReplicatedStorage"), game:GetService("ServerStorage") }
local areas: { [string]: { number } } = {}
local totals: { number } = { 0, 0, 0 }
local meshUses: { [string]: number } = {}

-- Area = service plus the next two levels, for example "Workspace/Map/Shop".
local function areaOf(inst: Instance): string
	local names: { string } = {}
	local current: Instance? = inst.Parent
	while current ~= nil and current ~= game do
		table.insert(names, 1, current.Name)
		current = current.Parent
	end
	return table.concat(names, "/", 1, math.min(#names, 3))
end

local function bump(inst: Instance, kind: number)
	local key = areaOf(inst)
	local tally = areas[key]
	if tally == nil then
		tally = { 0, 0, 0 }
		areas[key] = tally
	end
	tally[kind] += 1
	totals[kind] += 1
end

local seen = 0
for _, root in roots do
	for _, d in root:GetDescendants() do
		seen += 1
		if seen % 2000 == 0 then
			task.wait() -- keep Studio responsive
		end
		if d:IsA("BasePart") and not d:IsA("Terrain") then
			if d.Transparency >= 1 then
				if d.CastShadow then
					bump(d, SHADOW)
				end
			elseif d:IsA("MeshPart") then
				meshUses[d.MeshId] = (meshUses[d.MeshId] or 0) + 1
				if not d.CanCollide and not d:HasTag("NonSolid") then
					local model = d:FindFirstAncestorOfClass("Model")
					if not (model and model:FindFirstChild(d.Name .. "_COL", true)) then
						bump(d, NOCOL)
					end
				end
			else
				bump(d, PRIM) -- Part, WedgePart, TrussPart, UnionOperation and other non-mesh parts
			end
		end
	end
end

local out: { string } = {
	`Visible primitives {totals[PRIM]} | visible meshes without collision {totals[NOCOL]} | invisible helpers casting shadow {totals[SHADOW]}`,
}
local keys: { string } = {}
for key in areas do
	table.insert(keys, key)
end
table.sort(keys, function(a: string, b: string): boolean
	return areas[a][PRIM] + areas[a][NOCOL] > areas[b][PRIM] + areas[b][NOCOL]
end)
for i = 1, math.min(#keys, MAX_ROWS) do
	local t = areas[keys[i]]
	table.insert(out, `  {keys[i]}: primitives {t[PRIM]}, no collision {t[NOCOL]}, shadow helpers {t[SHADOW]}`)
end
if #keys > MAX_ROWS then
	table.insert(out, `  ... and {#keys - MAX_ROWS} more areas`)
end

local ids: { string } = {}
for id in meshUses do
	table.insert(ids, id)
end
table.sort(ids, function(a: string, b: string): boolean
	return meshUses[a] > meshUses[b]
end)
local foreign, unreadable = 0, 0
local checked = math.min(#ids, CREATOR_CHECKS)
if checked > 0 and game.CreatorId ~= 0 then
	for i = 1, checked do
		local assetId = tonumber(string.match(ids[i], "%d+"))
		local ok: boolean, info: any = false, nil
		if assetId ~= nil then
			ok, info = pcall(MarketplaceService.GetProductInfoAsync, MarketplaceService, assetId, Enum.InfoType.Asset)
		end
		local creator: any = if ok and typeof(info) == "table" then info.Creator else nil
		if typeof(creator) ~= "table" then
			unreadable += 1
		elseif creator.CreatorTargetId ~= game.CreatorId or creator.CreatorType ~= game.CreatorType.Name then
			foreign += 1
			table.insert(out, `  NOT THE OWNER'S UPLOAD: {ids[i]} used {meshUses[ids[i]]} times, uploaded by {creator.Name}`)
		end
		task.wait(CHECK_PAUSE)
	end
	table.insert(out, `Unique MeshIds {#ids}; creator checked on the {checked} most used: {foreign} not uploaded by the game owner, {unreadable} unreadable`)
else
	table.insert(out, `Unique MeshIds {#ids}; creator check skipped (unpublished place, no meshes, or CREATOR_CHECKS = 0)`)
end

local clean = totals[PRIM] == 0 and totals[NOCOL] == 0 and totals[SHADOW] == 0 and foreign == 0 and unreadable == 0
table.insert(out, if clean then "House-rule scan OK" else "House-rule scan: findings above")
print(table.concat(out, "\n"))
