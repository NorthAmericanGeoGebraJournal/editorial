--- lists-to-outline.lua
--- Render every Markdown bullet/ordered list using the NAGJ `outline`
--- environment, so authors write normal Markdown and get the house list style.
---
--- A top-level bullet list becomes \begin{outline} ... \1 ... \2 ...; an ordered
--- list becomes \begin{outline}[enumerate]. Nesting is emitted with increasing
--- \1 \2 \3 depth. The outline package fixes the marker style (bullet vs number)
--- per environment, so a list whose nested sublist is a DIFFERENT type renders
--- that sublist in the parent's marker style -- uniform-type lists (the common
--- case) are exact.

local function item_to_latex(blocks)
  -- Render an item's own (non-list) blocks to a LaTeX string.
  if #blocks == 0 then return "" end
  local s = pandoc.write(pandoc.Pandoc(blocks), "latex")
  return (s:gsub("%s+$", ""))
end

-- Recursively turn a List element into outline body lines at the given depth.
local function walk(list, depth, lines)
  for _, item in ipairs(list.content) do
    local own, subs = {}, {}
    for _, blk in ipairs(item) do
      if blk.t == "BulletList" or blk.t == "OrderedList" then
        subs[#subs + 1] = blk
      else
        own[#own + 1] = blk
      end
    end
    lines[#lines + 1] = "\\" .. depth .. " " .. item_to_latex(own)
    for _, sub in ipairs(subs) do
      walk(sub, depth + 1, lines)
    end
  end
end

local function to_outline(el)
  local opt = (el.t == "OrderedList") and "[enumerate]" or ""
  local lines = {}
  walk(el, 1, lines)
  local body = "\\begin{outline}" .. opt .. "\n"
            .. table.concat(lines, "\n") .. "\n\\end{outline}"
  -- Return the RawBlock and `false` so the top-down traversal does NOT descend
  -- into it again (we already handled the nested lists ourselves).
  return pandoc.RawBlock("latex", body), false
end

return {
  {
    traverse = "topdown",
    BulletList = to_outline,
    OrderedList = to_outline,
  },
}
