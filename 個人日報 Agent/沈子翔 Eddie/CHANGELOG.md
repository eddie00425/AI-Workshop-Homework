# CHANGELOG

## 2026-07-29

### 今天天氣真好

## 2026-07-28

### 新增 generation-flow.md（執行期施工手冊）+ 執行內容去重

- 新開 [generation-flow.md](generation-flow.md)：執行期把 frame spec + library 建成 Figma frame 的施工手冊（讀者：生成器）。含 Model（detach 只在最外層做一次；內層 frame 直接編輯、instance 直接填值）、Workflow（8 步：讀 spec → 取用 → optional → 填值 → 綁變數 → 分段上色 → 收尾驗證對 spec → frame 名稱設空白）、Rule（變數綁定：A Device 全域慣例 / B width·gap 按圖施工；分段上色）
- 執行內容收斂到 generation-flow.md，各來源改指標保 SSoT：
  - [spec-guide.md](spec-guide.md)：刪 Appendix「執行模型」pseudocode，讀法（line 9）與 Model（line 22）直指 generation-flow.md
  - [design-token.md](design-token.md)：「segments 編譯虛擬碼」收成一行指標，指 generation-flow.md「分段上色」；本表只留短碼 ↔ key 對照
  - [CLAUDE.md](CLAUDE.md)：參考文件表新增 generation-flow.md 指標（執行期產出 / 修改 frame 時讀）
- [spec-guide.md](spec-guide.md)：variable 佔位符統一 `{變數名}` → `{Variable Name}`

### write-copy skill：章節名 / 代碼引號細則修正

- [write-copy SKILL.md](.claude/skills/write-copy/SKILL.md)：用字細則改為「章節名用「」，代碼 / 術語 / 識別字用反引號」（原本寫反成章節名用反引號）；收尾自查同步

## 2026-07-23

### 新增 copy-guide.md（UI 文案規範）

- 新開 [copy-guide.md](copy-guide.md)：設計稿裡給使用者看的介面文字（UI copy）書寫規範，首條「中文與英數間留半形空格（盤古之白）」；頂部 Scope 與 `/write-copy`（文件自身文風）切分受眾
- [CLAUDE.md](CLAUDE.md)：參考文件表新增 copy-guide.md 指標（生成 / 填寫 spec 文字值時讀）

### design-token.md：Layout variables 補 hex key

- Layout variables 表新增 `key` 欄，9 個變數補上 `.key`（Page Width / Main Width / Card Grid 10col / Form Gap / Collapse Wrap Gap / Card Padding / Input Gap / Collapse Bottom Padding / Device），供 `importVariableByKeyAsync`
- 刪除 library 查無的死條目 `{Data List Width 1col}`（全 repo 僅本表引用、無節點使用）

### 信貸 s3 身分驗證頁：spec 定案 + 生成到 Figma

- [信貸-s3-loan-apply-newnew-01.yaml](projects/AI%20生成設計稿測試/frames/信貸-s3-loan-apply-newnew-01.yaml)：Field Set Layout `2-1`（1/2 · 1/2 兩等欄）確認、產出位置確認（node 166:3450 右側）
- 依 spec 生成到 Figma（node 208:3677，來源右側），library-first：detach Base → 中間換 Main 容器；6 欄位（radio 群 / read-only / help text / date / select / input）；notification 與 pre-action-note 分段上色（G500）；Form 寬度綁 `{Card Grid 10col}`、gap 綁 `{Form Gap}`

## 2026-07-22

### 專案去識別化：對外名稱改用 AI Gen Figma

- [CLAUDE.md](CLAUDE.md)：主標題與角色定義改用專案名「AI Gen Figma」，設計系統改以「本設計系統」泛稱
- [glossary.md](glossary.md)、[todo.md](todo.md)、[audit-library skill](.claude/skills/audit-library/)：內文的特定設計系統名一律改泛稱、移除版本號

## 2026-07-21

### done 流程措辭精簡

- [CLAUDE.md](CLAUDE.md)：done 規則標題與第 3 步（`git status` 巡檢）措辭精簡，意思不變

### done 流程加 git status 巡檢

- [CLAUDE.md](CLAUDE.md)：done 流程新增「commit 前 `git status` 巡一遍」步驟——確認本批該 stage 的都在，未 stage 的孤兒改動不默默掃進來、回報使用者決定（保留選擇性 commit）

### glossary tail id 定義去 why

- [glossary.md](glossary.md)：tail id 詞條砍掉「為何只取尾段」的原由（`跨變體穩定`、與 nested prop 對比那段），只留純定義（glossary 是定義處，why 不進）

### node-guide rebuild per-child 樣式 bullet 精簡

- [node-guide.md](node-guide.md)：`children` 樣式覆寫（`padding_top`）那條 bullet 依 write-copy「Tell, not explain」收成純規則（機制說明與重複範例去掉，具體例仍在上方 rebuild.children code block）

### refs 改指標制（pointer；廢 refs/ 資料夾）

- **來源改存指標（pointer），不複製 binary 進 git**：`refs/` 資料夾 → 專案 `refs.md`（每筆一行 `型別｜定位｜描述｜URL`）。來源住原地（Figma / Drive / Notion），spec 用連結指過去；Figma 連結最佳，AI 走 MCP `get_screenshot` 直接讀（實測讀得到 node 166:3450）。無線上家的來源先放上線再指，不落 binary
  - 新增 [refs.md](projects/AI%20生成設計稿測試/refs.md)（s3 來源指向 Figma node 166:3450）；刪 `refs/` 資料夾與其 png
  - [CLAUDE.md](CLAUDE.md)：專案結構、生成流程 step 2、Rules「來源指標先寫進 refs.md」全對齊指標制
  - [spec-guide.md](spec-guide.md)「來源標註」：範例改 Figma node 指標格式
  - [信貸-s3-loan-apply-newnew-01.yaml](projects/AI%20生成設計稿測試/frames/信貸-s3-loan-apply-newnew-01.yaml) 來源行改指 Figma node；[todo.md](todo.md) 生成項對齊

### Field Set Layout 校準（截圖實證）+ Input Group 雙 Field Set 組合模式 + structure/description 界線 + swap prop typo/casing 修正

- **[field-set.yaml](components/field-set.yaml) Layout 描述重寫為「列 × 欄寬」**：同列各欄寬以「·」分隔寫比例、多列以「｜」分隔。經 Figma 截圖**實證**校正原本憑值名臆測的錯誤（`2-2`＝1/3·2/3、`3-2`＝1/4·1/4·1/2 地址、`3-3`＝1/2·1/2 ｜ 滿寬、`4-2`＝上列三欄 ｜ 下列滿寬 等）。分「啟用（7 個單列積木）」與「暫不使用（9 個多列 / 特殊，改用 Input Group 組合）」；冗餘欄位數註記清掉（第一碼已是欄位數）
- **Input Group 雙 Field Set 組合模式**（Eddie 提案）：多列排版改由 Input Group 疊兩個 Field Set 達成，取代 Field Set 的多列 Layout 變體
  - [input-group.yaml](components/input-group.yaml)：`children` 補第 2 個 Field Set（optional、預設 hidden、自帶 `padding_top: "{Input Gap}"` 當列間距，frame gap 維持 0）；`field_set` 可寫單一 map 或清單（上限 2）；完整版 spec_example（label / swap / text 全貌，戶籍地址 = 2-1 radio + 3-2 地址；含 `as:` swap 故整段註解避 lint 誤報）
  - [design-token.md](design-token.md)：登記 `{Input Gap}` 16（`search_design_system` 驗真名——查變數比 `get_variable_defs` 讀隱藏節點可靠）
- **[node-guide.md](node-guide.md) structure / description 界線**（首次明文）：structure 只放圖層樹；屬性與 VARIANT 各值的含意寫進該 prop 的 `description`。另補 rebuild.children per-child 樣式覆寫（`padding_top` 可綁 variable）
- **[spec-guide.md](spec-guide.md)**：新增「field_set 一或多列」段（map 或 list）；修 help_text schema bug（誤用 `hint: show/text` → 正確 `"Show 灰色文字"` / `"灰字內容"`，源頭在此擴散到 s3，doc 兩處都修）
- **Field Set swap prop typo / 大小寫修正**（Figma 已改名，同步 repo）：`Swap Textfeild2 → Swap Textfield2`、`Swap textfield3..8 → Swap Textfield3..8`（id 全不變，`use_figma` 讀 `componentPropertyDefinitions` 確認）。同步 field-set / input-group / spec-guide / s3 frame；W5b frame 照「不回改 frames/」保留原字
- **[信貸-s3-loan-apply-newnew-01.yaml](projects/AI%20生成設計稿測試/frames/信貸-s3-loan-apply-newnew-01.yaml)**：修 help_text schema + `Swap Textfield2`；來源標註接真實 refs 檔名；**C**（radio `Layout "2-1"`＝兩欄等寬）已驗證。生成仍待 Eddie 提供目標 page URL
- **[todo.md](todo.md)**：新增「後門：spec 層 style override」段（受控後門 + 設計師同意留成可見標記，與 override 圖釘不地圖之討論同源）；field-set descriptions 精修項

## 2026-07-17

### notification 修正（raw node → nested prop）+ node-guide 分類守則 + 更新流程補平 + s3 spec 首版

- **[notification.yaml](components/notification.yaml)：title / body_text / text_link 從 raw node 改為 nested prop**（讀 `componentProperties` 驗過的真 id）。三者都是 property，只是長在內層 `.w/ icon_website` 卡片上、未暴露到頂層 set（頂層只有 `Configurations` / `Mode` 兩軸）：`title＝Title#11408:26`、`body_text＝Content#11408:27`、`text_link＝placeholder#5986:0`（`.w/ icon_website > TextLink-Small`，兩層）。body / link 顯示由 Mode 變體內建 boolean 控制，生成端不手設
  - **根因**：原本用 `get_design_context` 判斷型別，它看不到 exposed nested prop（只渲染成裸 `<p>`），把 nested prop 誤判成 raw node
- **[node-guide.md](node-guide.md) 兩處規則補強**（防同款誤判）：
  - 「設值的三種存取路徑」加**偵測守則**：判斷前先讀 `componentProperties`（`use_figma`，含 nested）；查得到 property 就是 component / nested prop，確認完全沒 property 才落 raw node。別靠 `get_design_context` / 畫面 dump 判斷
  - **新增 / 更新流程改三來源分工**：`get_metadata` 取圖層結構、`get_design_context` 看畫面 / 樣式 / 頂層 props、`use_figma` 讀 `componentProperties`（含 nested）。**component 一律讀 `componentProperties`、不設條件**——補平原本「新增有讀、更新沒讀」的不對稱（更新流程缺這步，正是這次誤判的結構性病灶）
- **[信貸-s3-loan-apply-newnew-01.yaml](projects/AI%20生成設計稿測試/frames/信貸-s3-loan-apply-newnew-01.yaml) 首版**：s3 身分驗證頁 frame spec。W5b `as:` 語法首次實戰——身份驗證方式（radio 群）/ 身分證字號（read-only 遮罩 Input）/ 出生年月日（Date Select）/ 銀行名稱（Select）/ 行動電話・銀行帳號（Input）全走「槽名當 key + `as:`」；notification 內文走分段上色綠字。**A**（置中「請輸入身分資料」標題，無 library slot）依 Eddie 決定不做；**B**（notification）已解；**C**（radio 兩欄 `Layout "2-1"`）待驗證

## 2026-07-16

### swap 設值段 write-copy 打磨 + write-copy 補破折號細則

- **[spec-guide.md](spec-guide.md)「swap 設值」白話化**：兩種寫法正名為 **只換型別 / 換型別並設值**（本質是「設換入元件的值」，變體只是其一，不再叫「改狀態」）；範例補齊「只換型別 → 設值 → 設值再切變體」三情況；`map` → 「一組欄位」、移除 `variant prop` 詞、`＋` → 並
- **[node-guide.md](node-guide.md) / [field-set.yaml](components/field-set.yaml)**：`map` → 「一組欄位」對齊
- **[write-copy](.claude/skills/write-copy/SKILL.md) 用字細則新增「不用破折號 `——`」** + 收尾自查（全 repo 既有 46 個 `——` 未掃，另開清掃）

### W5b swap 設值定案（INSTANCE_SWAP 槽值：字串 or `as:` map）+ CLAUDE.md 寫作立場 / 排版措辭校正

- **W5b swap 設值定案**：INSTANCE_SWAP 槽（`Swap Textfield1`…）的值兩形態——只換型別＝字串（`"Swap Textfield1": "Select"`）；換型別＋設值＝map（`as:` 標型別 + 換入元件的扁平 props）。**槽名當 key**（槽名唯一，多槽各自一個 map、值不跨槽撞 key），否決了原設想的 `inputs:` list。換入元件的 nested prop / raw node 不論幾層深，皆由該元件 YAML 攤成扁平友善鍵，spec 只寫值、不重寫巢狀樹
  - [spec-guide.md](spec-guide.md)：新增「swap 設值」段（兩形態 + field_set checkbox 範例 + 深度吸收 / 帶色走分段上色兩條）；Props 段 swap bullet 補指標；常見錯誤加一列（props 平攤在 field_set 層會多槽撞 key → 收進槽 map）
  - [node-guide.md](node-guide.md)：INSTANCE_SWAP 段補一行指標 → spec-guide「swap 設值」（機制留 node-guide、spec 寫法在 spec-guide，SSoT 不破）
  - [field-set.yaml](components/field-set.yaml)：spec_example 加「換型別＋設值」的 `as:` map 範例
  - [todo.md](todo.md)：W5b 打勾
  - 新增深度驗證範例 [W5b field-set checkbox 深度範例.yaml](projects/AI%20生成設計稿測試/frames/W5b%20field-set%20checkbox%20深度範例.yaml)（4 欄 checkbox，「其他」展開補充輸入 5 層深、帶色，證明 spec 仍只寫一層扁平鍵）
- **[CLAUDE.md](CLAUDE.md) 校正**：
  - 「Tell, not explain」收緊——「不寫推理長篇」→「不解釋為什麼，不寫原由」
  - 排版段刪「spec 不需重寫」、「排版**規則**」→「排版**樣式**」、「由 detach 繼承」→「detach **後**繼承」：釐清 detach 繼承是**樣式基線**（可往上覆寫），非「禁止覆寫」的鎖。覆寫走既有 `raw_nodes` 退路（優先序：先用 library 露出的 property，沒有才 raw 覆寫、且 spec 顯式寫出）

## 2026-07-15

### 存取路徑欄位 B 方案：`nested_overrides` 拆成 `nested_props` + `raw_nodes` + `id`→`tail_id`

- **`nested_overrides` 一鍵拆成兩個自陳鍵**：[node-guide.md](node-guide.md) 與各 yaml 把原本靠有無 `prop:` 分辨兩型的 `nested_overrides`，拆成 `nested_props`（值是 nested component 的 property）與 `raw_nodes`（值無 property、直接改 node）。`props` 維持不變（三者非對等、不跟著改名）。遷移：[input.yaml](components/input.yaml) / [select.yaml](components/select.yaml) / [button-group.yaml](components/button-group.yaml) → `nested_props`；[notification.yaml](components/notification.yaml) / [modal.yaml](templates/modal.yaml) → `raw_nodes`（仍舊 name-path 風格，待日後遷 `tail_id`）；[button.yaml](components/button.yaml) 註解指標同步
- **raw node 解析錨 `id` → `tail_id`**：[date-select.yaml](components/date-select.yaml) `173:37024`、[radio-button-type.yaml](components/radio-button-type.yaml) `6612:31546`、[checkbox-button-type.yaml](components/checkbox-button-type.yaml) `6647:109163`。更名點出「只記尾段」的本質——完整 id 形如 `I{instance};…;{tail_id}`，中段是變體專屬的內層 instance id、記死會跨變體失效，故只比對尾段 `findOne(n => n.id.endsWith(";"+tail_id))`
- **「設值的三種存取路徑」段重寫**：去 2×2 表格、去「軸」框架，改純散文分別定義 component prop / nested prop / raw node 三條路徑，各對一個 yaml 欄位（一眼可掃）
- **撞尾段防線**：[node-guide.md](node-guide.md) 補 raw node 尾段撞 id 的守門——同一子元件在元件內被引用 2 次以上時兩份尾段相同、`findOne` 會同時命中，標 ⚠️「請設計師把文字設為 Props」
- **glossary 新增 `tail id` 術語**：[glossary.md](glossary.md) 收純定義（尾段、跨變體穩定、有別於 prop id 與完整 node id）；why（為何不記中段）退場、不進 glossary 也不開 appendix，設計理由留在 git / CHANGELOG 歷史，[node-guide.md](node-guide.md) 拿掉「原因見 glossary」指標
- **[lint.py](.claude/skills/audit-library/lint.py)**：`flatten_keys` 同時攤平 `nested_props` / `raw_nodes` 兩鍵

### write-copy 補比較符號細則 + 全 repo 清 `≥`

- **[write-copy](.claude/skills/write-copy/SKILL.md) 新增用字細則**：敘述句不用 `≥` `≤` `=` `<` `>` 等比較符號，改寫成以上 / 以下 / 等於 / 大於 / 小於（路徑分隔 `>`、箭頭 `→` 不算）；收尾自查同步
- **清掉現存 `≥`**：[glossary.md](glossary.md) / [spec-guide.md](spec-guide.md) / [write-doc/SKILL.md](.claude/skills/write-doc/SKILL.md) / [audit-glossary/SKILL.md](.claude/skills/audit-glossary/SKILL.md) 的「≥2」「≥5」改成「2 以上」「約 5 次以上」。`CHANGELOG.md` 為歷史記錄不回改

## 2026-07-14

### raw node 改用 node id 為解析錨（target 對齊 nested prop）+ 文件寫作規範

- **raw node 存取路徑 id 化**：[node-guide.md](node-guide.md) raw node 段改寫——記 `id`（該 node 在元件定義裡的 id）為解析錨，生成端 `findOne(n => n.id.endsWith(";"+id))` 取得節點。`target` 降為選填、只寫值所屬的 nested component 名，與 nested prop 的 `target` 對齊；兩者差別回到 `prop:` 有無（有→property id 走 setProperties，無→node id 走 findOne）
  - **連帶移除整套 autoRename gate**（原 ⚠️ 規則 / gate 句 / `autoRename` 註解）：id 不看 layer name，raw node 不再依賴圖層名，改名或 autoRename 都不影響；撞名問題隨 id 唯一性退休
  - 「三存取路徑」表 raw node 列、「能用 property 就用 property」規則句同步（原述 raw node「綁圖層路徑、較脆弱」已不成立）
- **回填三顆 raw node 的 `id`**：[date-select.yaml](components/date-select.yaml) `173:37024`、[radio-button-type.yaml](components/radio-button-type.yaml) `6612:31546`、[checkbox-button-type.yaml](components/checkbox-button-type.yaml) `6647:109163`（實測 instance 子節點 id 形如 `I{instance};…;{id}`，尾段即元件定義 node id）；target 從完整圖層路徑縮成 nested component 名
- **[CLAUDE.md](CLAUDE.md) 新增「文件寫作立場」節**：把 write-copy 走 Reference Writing 的四條核心（結論先講 / 自成一則 / Tell not explain / 術語一致）拉進常駐 context，塑形第一版草稿；完整原則仍指回 `/write-copy`
- **[write-copy](.claude/skills/write-copy/SKILL.md) 補用字細則（正反例）**：不用 `+` 當連接詞、不用資料結構行話（葉 / 樹）當比喻、代碼術語用反引號不用「」、抽象難懂時直接給實例；收尾自查同步

## 2026-07-13

### W4.5：新增 Checkbox Button Type 元件 YAML + Placeholder→Text 改名（radio / checkbox）

- **[checkbox-button-type.yaml](components/checkbox-button-type.yaml) 新增**：單顆多選選項，與 Radio Button Type 同家族（Selected + State 兩軸），經 Field Set Swap 排成複選群。component_key `0dc87155760cd9752523f90d4fd0d749e8777087`、node `175:68437`
  - 與 Radio 三處差異：可多顆同時 On（複選）、State 多 `Expand Error`（8 態 vs 7）、內層多 `Show Input Cursor` boolean（由 State=Expand 內建、生成端不設）
  - label 走 nested prop、expand_input（請輸入）走 raw node（同 Radio）
- **⚠️ node_id 修正**：todo 原記 `11319:394` 有誤，實際 set 為 `175:68437`（與 Eddie 提供的 URL 一致）
- **[radio-button-type.yaml](components/radio-button-type.yaml) + checkbox：內層文字 prop `Placeholder` → `Text`**：Eddie 在 Figma 端改名（Placeholder 語意是「會消失的灰提示」，實裝的卻是永遠顯示的選項標籤，語意錯位）。id 不變（radio `6608:13`、checkbox `6647:1`）→ 改名沒斷 binding。四顆表單輸入元件內層文字 prop 至此全叫 `Text`（Input / Select / Radio / Checkbox），家族命名對齊。移除原 ⚠️ 註記，`last_verified` → 2026-07-13
- **[_index.yaml](components/_index.yaml)**：補 Checkbox Button Type 一行（排在 Button Group 後）
- **[todo.md](todo.md)**：W4.5 + W6 打勾（主線 W1–W6 全完成，剩 W5b + 生成 s3）
- **/audit-library 三段全過**：Part A lint 0/0（33 節點）；Part B Figma 對照全一致；Part C 探測檔（`ShAeuYvfMSAHn02VDMUo9J`）import 成功＝已發佈，Tier 2 指紋一致＝最新版

### W4：新增 Date Select 元件 YAML（date-select.yaml）

- **[date-select.yaml](components/date-select.yaml) 新增**：單一日期選擇框，與 Select / Input 同家族（State + Text configurations 兩軸），經 Field Set Swap 放入。component_key `52f1ad7e5246fe33e64281a9aa4f33ebc942d0f3`、node `173:36749`
- **文字走 raw node（非 nested prop）**：內層 `.Date Select` instance 未暴露任何 component property（與 Select 的 `.Select` 有 Text prop 不同），日期文字只能直改內層 `Inner Wrap > Text` raw node；右側日曆 icon（Icon/L017）固定、無 swap。經 Eddie 確認此為 library 前人設計、無須與 Select 對齊
- **[_index.yaml](components/_index.yaml)**：補 Date Select 一行（排在 Data List Row 後）
- **[todo.md](todo.md)**：W4 打勾；W6 註記已含 Date Select（剩 W4.5 checkbox-button-type）
- **/audit-library 三段全過**：Part A lint 0/0；Part B Figma 對照（名 / props / key / 結構）全一致；Part C 在探測檔（`ShAeuYvfMSAHn02VDMUo9J`）import 成功＝已發佈，Tier 2 指紋一致＝最新版

### Input node_id 修正（回 Figma 對照發現舊帳）+ Clear Icon 去前導空格

- **[input.yaml](components/input.yaml) + [_index.yaml](components/_index.yaml) node_id `11257:347` → `40:61910`**：回 Figma re-verify 時發現舊 node_id 已失效（Select / Button 抽查正常，故非全檔改版）。component_key 不變（`e45f4452…`）證明元件沒重建——是 node_id 本來就記錯的舊帳，非本次改名所致。figma_link 同步更新
- **[input.yaml](components/input.yaml) clear_icon `prop` `" Clear Icon"` → `"Clear Icon"`**：Eddie 在 Figma 端把該 boolean 屬性名的前導空格改掉，YAML 同步、拿掉 ⚠️ 註記。（註：MCP 讀屬性名會正規化成 camelCase、吃掉空格，此欄採信 Figma 面板人工確認）`last_verified` → 2026-07-13
- **教訓**：lint 只驗「index vs 檔案」內部一致，兩邊同錯（`11257:347`）會放行；「內部一致但 Figma 上不存在」只有回 Figma 對照抓得到（/audit-library 的 Figma 階段）。其他 node_id 可能有同款舊帳，待全面重掃

### node-guide INSTANCE_SWAP 段 write-doc / write-copy 體檢

- **[node-guide.md](node-guide.md) 結構修正**：通用 props 欄位 bullet（`bound_variable`／可讀名／撞名／待補／分段上色）原被困在 `##### INSTANCE_SWAP` 專節「之下」，被誤讀成 INSTANCE_SWAP 專屬——移到專節「之前」，INSTANCE_SWAP 改當 Props 格式的收尾子節
- **[node-guide.md](node-guide.md)「常見錯誤」補反例**：INSTANCE_SWAP 兩個踩雷史（swap 值填 node id、以為只能填 preferred_values 清單內）補 ✗/✓ 一列
- **[node-guide.md](node-guide.md) swap 值 / preferred_values 兩 bullet write-copy 改寫**：去粗體濫用（雙粗體 → 0，`preferred_values` 改行內 code 對齊 `bound_variable`）、「餵 setProperties」→「傳入 setProperties」（API 語氣）、component／元件用字統一
- **[spec-guide.md](spec-guide.md) swap 值去重（SSoT）**：拿掉重述的機制（`component_key`→`defaultVariant.id`），改指回 `node-guide.md`「INSTANCE_SWAP」；機制單一來源收在 node-guide
- lint 0/0

### preferredValues：node-guide 補「非限制」+ glossary typo 修

- **[node-guide.md](node-guide.md) preferred_values bullet 補「只排序、不限制，清單外也可 swap」**：field-set.yaml 每個 Swap prop 底下的 `preferred_values` 清單結構上像 whitelist，補一句釘死「preferredValues 不阻擋」，防讀成封閉集合（散文已用「推薦」不誤導，殘留風險只在資料結構的觀感）
- **[glossary.md](glossary.md) preferredValues typo**：`prefered` → `preferred`

### INSTANCE_SWAP / preferredValues 說明再精簡（措辭收斂）

- **[node-guide.md](node-guide.md) INSTANCE_SWAP swap 值瘦身**：拿掉「非 node id」與「node id 各檔獨立編號、屬編譯期產物」等重複補述，只留「填 component 名 → 生成端由 `component_key` import 取 `defaultVariant.id`」核心；`default` 範例註解同步縮短
- **[spec-guide.md](spec-guide.md)**：swap 值「寫 component 名（name）」措辭對齊，去掉「非 node id」贅述
- **[glossary.md](glossary.md) preferredValues 定義收斂**：縮成「Figma swap instance 的 preferred instance 清單，記在 node YAML `preferred_values`」
- **[button-group.yaml](components/button-group.yaml)**：移除 primary/secondary 的 nested prop 設值路徑說明註解（node-guide「設值的三種存取路徑」已載）

### INSTANCE_SWAP swap 值改寫 component 名 + preferredValues 正名（修「白名單會被擋」誤解）+ node-guide Props 精簡

- **preferredValues 正名（修正認知錯誤）**：原文件把 INSTANCE_SWAP 的 `preferred_values` 寫成「白名單、換清單外會被 Figma 擋掉」是錯的——`preferredValues` 只是 swap 選單的 UI 推薦、不阻擋，清單外元件也能換。全 repo 把此概念的「白名單」改成 `preferredValues`（node-guide / field-set / todo），列入 [glossary.md](glossary.md)「preferredValues」。lint known-vars 等其他「白名單」概念不動
- **INSTANCE_SWAP swap 值改寫 component 名**：spec 與 node YAML `default` 一律寫 component 名（如 `"Swap Textfield1": "Select"`），不寫裸 node id——node id 各檔獨立編號、是 library 檔的脆弱編號（拿到產出檔不成立），屬編譯期產物；生成端由該元件 `component_key` `import` 後取 `defaultVariant.id`。非預設狀態（error-text 等）swap 到預設後再設 variant prop、不需該 variant id。改動 [node-guide.md](node-guide.md) swap 值規則 + 兩 yaml 範例、[field-set.yaml](components/field-set.yaml) 8 個 `default:` 與 spec_example、[spec-guide.md](spec-guide.md) Props 段
- **node-guide Props 格式精簡**：`可讀名#id` 組成規則原上下重複兩處 → 收一處；「type 種類」表 → 一行列舉四型；INSTANCE_SWAP 小節從雙表格 → 兩個 bullet + 兩個 yaml 範例
- **todo W5c 標完成**：INSTANCE_SWAP 設值方式定案（承接同日「白名單結構化」那筆遺留的待重新設計項）

### Field Set Swap 白名單結構化 + node-guide INSTANCE_SWAP 專節 + 修失效交叉引用

- **修失效交叉引用**：`select.yaml` / `input.yaml` 原引用「見 field-set.yaml『Swap 輸入型別』」，但該段落不存在——改成「見 field-set.yaml」（不指向特定段落，避免欄位改名再斷）
- **[field-set.yaml](components/field-set.yaml) 各 Swap prop 補 `preferred_values`**：INSTANCE_SWAP 的可替換白名單，實查 Figma preferredValues 取得（Input / Select / Radio Button Type / Checkbox Button Type / Date Select 五個 component_set）。最終收斂成**純元件名清單**——component_key 留在各元件自身 YAML（SSoT，不重寫）、不記 status。8 個 Swap prop 共用白名單，僅第一個完整列出，其餘寫 `同 Swap Textfield1`。`last_verified` 更新到今天
- **[node-guide.md](node-guide.md) INSTANCE_SWAP 從 Appendix 升為 Props 專節**：新增「type 種類」表（VARIANT / BOOLEAN / TEXT / INSTANCE_SWAP 各自的 id 有無、值格式）；INSTANCE_SWAP 小節用表格切開「swap 值＝目標 variant node id」與「白名單＝元件名引用」兩個不同識別符
- **[radio-button-type.yaml](components/radio-button-type.yaml) write-copy 體檢**：消掉「經 Field Set 的 Swap 放入」在 `用途` 與 `spec_example` 重複兩次，對齊 select.yaml
- **[todo.md](todo.md)**：W5 拆成 a（preferred_values 已完成）/ b（spec `inputs:` 表達待定）/ c（INSTANCE_SWAP 設值方式待重新設計，目前 spec 寫裸 node id）；新增 W4.5 追蹤查證時發現、原規劃漏掉的 Checkbox Button Type

## 2026-07-12

### write-copy 改走 Reference Writing 路線

- **原則調整**：「白話易懂：非必要不用術語」→「術語精準：一律用 glossary 正式名稱」——reference 文件靠固定字串被查到，迴避術語反而查不到
- **新增「自成一則」原則**：每段要能被單獨查到、單獨看懂，不依賴讀者記得前段內容
- **固定順序簡化**：「Definition → Usage → Scenario → Reason（可選）」→「Definition → Usage → Example」，拿掉容易寫成小故事的 Scenario，Reason 降為非必要且要跟定義分開寫
- **收尾自查同步更新**：新增「結論先講，沒鋪陳？」「自成一則，不必往前翻？」，拿掉教學語氣殘留（首先 / 接著 / 你可以先…然後…）

## 2026-07-10

### W3 Select 元件 + input.yaml 對稱精簡（write-copy / write-doc 打磨）

- **新增 [components/select.yaml](components/select.yaml)**：component_set 兩條 variant 軸（State + Text configurations），與 Input 同家族——文字 / 箭頭 / 搜尋開關的 property 在內層 nested component `.Select` 上（非外層 set），走 nested prop
- **記錄 disabled / read-only 耦合**：Select 把 disabled 與 read-only 併成同一個 State 值，靠 `Text configurations` 分——`disabled = placeholder-text`（未選）、`read-only = select-text`（已選），兩者非獨立、互相耦合
- **_index.yaml 補 Select**；lint 0/0（登記節點 30→31）
- **input.yaml 對稱精簡**：頂部概觀併行、砍掉與 nested_overrides 重複的 property 位置說明、description 折行、spec_example 去重複句，與 select.yaml 風格對齊
- **todo.md 移除 W1–W3**（Input / Radio Button Type / Select 皆已完成），W4–W6 待做

### 移除 enhancement.md（e2e 踩雷教訓已吸收進主文件）

- **刪除 `enhancement.md`**：盤點後確認 P1–P4 踩雷教訓大多已吸收——P2/P3（property id 現讀 / nested instance 改字）收進 node-guide.md「設值的三種存取路徑」；P4（跨檔不可複製 frame）收進 node-guide.md「三種取用模式」+ Appendix。剩餘 O1–O5 優化項與 P1（`resize()` 兩軸鎖死）教訓尚未落地，之後如需再處理另開新項追蹤，不留這份暫存筆記
- 確認 todo.md 的「(enhancement)」字樣只是通用標籤、非檔案引用，CHANGELOG.md 為歷史記錄不回改，故刪除不需連動修改其他檔案

## 2026-07-09

### W2 Radio Button Type 元件 + write-copy 大幅打磨（去除粗體濫用、Reference 語氣、精簡改版）+ node-guide workflow 重編號

- **新增 [components/radio-button-type.yaml](components/radio-button-type.yaml)**：Selected（On/Off）× State（Default/Hovered/Error/Error-Hovered/Expand/Read-Only/Disabled）兩條 VARIANT 軸。文字設值分兩路——`label` 走 nested prop（內層 `.Radio Button Type` 的 `Placeholder#6608:13`，Figma 真名誤導、標註建議改名）、`expand_input` 走 raw node（Expand 態補充輸入框，無 property）
- **_index.yaml 補齊 Input（W1 漏登記）+ Radio Button Type**；lint 0/0（節點 29→30）
- **node-guide 新增 authoring SOP**：判斷 nested prop / raw node 要查 **nested component 自己的** `componentProperties`，不能只看 component 本身的 `componentPropertyDefinitions`（單一 component 或 set 皆同）——來自 Radio 的 `Placeholder` prop 藏在內層、外層看不出的實戰教訓
- **write-copy 新增第 6 條原則「Reference 不 Reasoning」**：規則句直接講能做什麼，限制當備註、不編進因果句；不影響「使用者主動問為什麼仍要好好教」
- **write-copy 全篇去除粗體濫用**：「粗體節制」允許「開頭固定粗一個詞」的舊寫法正是濫用的根源——改判準為「扁平列點不粗、互斥分支才粗」；随後 Eddie 進一步整份壓縮成 6 條原則 + 6 條自查（拿掉例子與說明，定位為速查卡）
- **write-copy description 觸發語意反轉**：從「使用者要求特定詞彙才啟用」改成「每次寫文件都主動套用，不必等要求」
- **node-guide「新增節點」workflow 拿 write-copy 實戰體檢**：Step 2 拆成獨立兩步——查結構（`get_design_context`，container/template 可另用 `get_metadata`/`use_figma`）與查 `componentProperties`（`use_figma`，含 nested component），原本擠在同句、又被錯誤分號黏住；後續步驟重編號 3–7。過程修正「同一件事的細節用分號、不同工具/目的的動作用句號」的判準

### Stage 2：新增 button.yaml + button-group 文字改 nested prop + 主線 W1–W6 進 todo

- **新增 [components/button.yaml](components/button.yaml)**：Button 元件本身（Button-L set，key `5b52500e34fa5e8b915c97d6d88fef239d2a8ccf`）。`Configuration`（filled/outlined/ghost/text）+ `State`（enabled/hovered/focused/disabled/Countdown/loading）兩條 VARIANT 軸 + `Text` component prop（id `2396:0`）——本專案第一個 TEXT 型 component prop（走 `props`，非 nested_overrides）
- **[button-group.yaml](components/button-group.yaml) primary/secondary 由 raw node 升成 nested prop**：實地查證 Button 有 `Text` component property（group 內每個 1st/2nd Button instance 都帶著），故正解是對內層 Button `setProperties`、非改底層 text node。修正舊 description 的錯述「無頂層 component property」。照 node-guide「能用 property 就用 property」定案
- **_index.yaml 補 Button**；lint 0/0（登記節點 28→29）
- **主線 W1–W6 進 [todo.md](todo.md)**：s3 身分驗證頁 library-first authoring（W1 input 已完成、W2–W6 待做、補完生成到 node 166:3450）。此前只活在對話裡、易隨分支遺忘，落檔追蹤

## 2026-07-08

### 新增 write-copy skill（句子層級寫作品質）+ write-doc 瘦身 + node-guide 定點修

- **新增 `.claude/skills/write-copy/SKILL.md`**：把「句子 / 段落層級的寫作品質」從 write-doc 抽成獨立輕量 skill——比 write-doc 輕，只管把字寫好、不管文件架構。5 原則：易理解（白話 / 載重句在前）、易讀（粗體節制 / 中英交雜節制 / 一句別扛太多維度）、精簡而完整（刪除測試 / 局部不重述）、用字一致、概念分層（Definition→Usage→Scenario→Reason）。含「動筆前先讀上下文」守則 + 收尾自查
- **write-doc 瘦身（SSoT 切分）**：prose 級規則（粗體節制 / 刪除測試）移出、改成一句指標指向 write-copy；原則區 + 自查清單「句子層級品質」條目都改連結、不重述。write-doc 專管文件架構、句子品質引用 write-copy
- **node-guide 跑一次 /write-doc（情境 B 定點修 4 處）**：① SSoT——「共用 X 差在 Y」的框架從「欄位順序」收掉、單一留在模式段（rebuild / detach）；② 補 nested_overrides 的 `kind` 定義；③ Appendix rebuild 主動選段落拆 run-on 長句；④ 「規則」整句粗體改只粗標籤。lint 0 ERROR / 0 WARN。過程實地驗證 write-copy 在 write-doc 流程中被啟用（句子級 B1/B2 由它掃出）

### node-guide「設值的三種存取路徑」+ W1 Input 元件（s3 身分驗證頁 library-first authoring 起步）

- **背景**：新 e2e 目標（s3 身分驗證頁）多了 project component YAML 未收錄的互動元件（單選群組 / 日期 / 下拉 / disabled input）。確認全是 Field Set 的 Swap 輸入型別（Input / Select / Date Select / Radio Button Type / Checkbox Button Type，keys 已抓）。Eddie 定調 library-first：先補 YAML 再生成。工作分 W1–W6，本次做 W1 + 打底
- **W1：新增 `components/input.yaml`**：Input component_set 兩條 variant 軸（State：enabled/hovered/focused/disable/read-only；Text configurations：placeholder/input/error…）+ 6 個 nested_override（text / prefix / suffix / search / icon_button / clear_icon，property 都在內層 `.Input`）。State 語意由 Eddie 補；` Clear Icon` 前導空格待 Eddie 修 Figma 後 re-verify
- **node-guide 新增「設值的三種存取路徑」**：`component prop`（property 在 component 本身 → `props`）/ `nested prop`（property 在 nested component 上、component 本身設不到 → `nested_overrides` + `prop:`）/ `raw node`（無 property、直接改節點 → `nested_overrides` 無 `prop:`）。附規則「能用 property 就用 property（component prop → nested prop），raw node 只當退路」——property 綁 id、免載字型、可重現
- **實測釐清 expose**：Figma「exposed nested instance」≠ component prop（母層 `setProperties` 找不到 key、仍須對 nested component 設）；expose 只是存取便利，YAML 不記（生成端一律「照 target 找到再設」）
- **nested_overrides 補 `prop` 形式 + 拆 id**：`prop`（可讀名）+ `id`（另存）+ `kind`，與 `props` 同慣例，不把 `名#id` 黏成一串
- **術語**：三路徑元件角色統一為 `component`（本身）/ `nested component`；描述性動作改白話中文（拿掉 traverse 等中英交雜）

## 2026-07-07

### Main container re-publish 驗證 + last_verified 刷新

- Eddie publish Main 空殼化後，實地 import 一顆全新 instance 驗證 Content 已清空（`childCount` 0）→ 印證上一筆 e2e finding「Main 帶 sample 是忘 publish」，且往後生成 import Main 直接得空 Content，「刪 sample Body」的 workaround 不再需要
- `containers/main.yaml` `last_verified` → 2026-07-07（實際比對過才刷日期）

### e2e 第四輪（detach/rebuild 分流定案後首次實地生成）+ 來源 refs 規則

- **e2e 第四輪**：新增 `frames/image to frame 04.yaml`（國泰世華信貸表單頁），純從 library 文件推導（不參考 frames 01–03）並實地生成到 Figma、截圖對照原圖 1:1。驗證三處落地——rebuild 容器（body / form）正確重畫而非 detach cascade、深層 Field Set 的 Device 綁定以顯式 `setBoundVariable`（variant alias）補回、綠連結 + 橘詐騙段走 segments 分段上色（G500 / O500）
- **修正 frame03 遺漏**：每個 input_group 顯式寫 `field_set: "Device": "{Device}"`（bound variable 不可省略；frame03 漏寫 field_set 曾被標為 bug）
- **e2e findings（Stage B 備忘）**：① Field Set 是 component_set → 用 `importComponentSetByKeyAsync` 取 variant，非 `importComponentByKeyAsync`；② `Show 2nd Button=false` 只隱藏祖層容器、內部 text 節點自身 `visible` 仍 true → nested override 改文字要用「有效可見性」定位；③ Main detach 帶 sample content 實為「library 改了忘 publish」，非 bug
- **來源 refs 規則（拆兩家、各一 SSoT）**：CLAUDE.md 定「生成 spec 前來源存進 `refs/`」的程序（生成流程 step 2 + Rules）；spec-guide.md 新增「來源標註」定 spec 檔頂 `# 來源：refs/xxx` 的撰寫慣例。判準＝存檔是「怎麼做」歸 CLAUDE、spec 標註慣例歸 spec-guide；兩事實雙向互指、無重述
- **todo.md**：移除擱置段 C-2 / C-5（此 session 前既有的工作區變更，一併提交）

## 2026-07-06

### todo.md 整理：Container 空殼化段落收尾

- Container 空殼化（路 1）段移除：C-1/C-7（已完成）+ C-3/C-4（不再於此追蹤）+ 決策 note 一併刪；知識未流失（detach/rebuild 兩路在 node-guide「為何分三種模式」、深層 leaf 綁定會掉在保留的 C-5）
- C-6 拉出成獨立段「rebuild schema：raw 節點引用 library style」；C-2 / C-5 移入新「擱置（pending）」段

### node-guide 內容欄位改用「取用模式」軸（F4）

- **F4 根治：分類軸 type → mode**：舊「Container 內容欄位（rebuild 模式）」名不副實（實含 Pack component + 容器），且同一個 Pack component 在「欄位順序」歸 Component、在「內容欄位」歸 Container，兩處打架。改用取用模式當軸——`instance / rebuild / detach` 三段，鏡射 Model「三種取用模式」；加一句 framing 帶出「共用欄位之外依模式分段」
- **detach 段合併**：detach 容器 + template 併為單一「detach 模式」段（共用 `structure` + `slot`，差在容器多 `layout` / `accepts`、template `spec_example` 必填）——與 rebuild 段「兩成員混一段」對稱（成員數 1 / 2 / 2）
- **欄位順序同步改 mode 軸（B）**：`共用 / instance 專屬 / rebuild 專屬 / detach 專屬`，一併收掉 Pack component 的歸類矛盾
- **交叉引用更新**：optional 三機制表指向「rebuild 模式」；lint `0 ERROR / 0 WARN`
- **用字：node-guide 內「容器」→「container」**（27 處：26 換 container、1 處泛指父層的「填滿父容器」改「填滿父層」）；Eddie 定調「指 container 本人就用 container」。範圍只 node-guide，glossary 等他檔暫留（刻意，日後再全 repo 統一）
- **Examples 不補 template / rebuild container 範例**：Rule 段 + 真檔已涵蓋，避免重複與維護漂移（Examples 只放代表 / 易錯者）
- **frame 03 檔名補空格**：`image to frame03.yaml` → `image to frame 03.yaml`（純改名，內容不變）

### node-guide 易讀性續修（F1–F6）

- **F1 detach 範例更新**：Examples「Container（detach 模式）」範例從 Form（已改走 rebuild）換成 Main，並補 Q2 的 `structure`（標 `(fillable)` Content 與 slot 所在層）→ 範例本身即一份合規 detach 容器
- **F2＋F3 欄位清單收斂 SSoT**：Workflow step 3 逐類列欄位（Container detach 漏 `structure` 的漂移源）改成指向 Rule「欄位順序」、不重列；Overview 表「內容欄位」欄放代表 signature，完整清單歸 Rule
- **F5 粗體節制**：三處雙粗體降為單粗 / 零粗（structure 原因、optional 三機制導言、Appendix rebuild 主動選擇）
- **F6 標籤統一**：欄位順序「Container 專屬 — detach / rebuild」→「專屬（detach / rebuild 模式）」，對齊 Template 與各 H3 的消歧義括號風格
- **F4 暫緩**：rebuild 段標題該不該叫「Container」待議
- **lint**：`0 ERROR / 0 WARN`

### Container 取用模式定案（rebuild）+ slot 填充目標（structure）+ node-guide 易讀性整頓

- **只有 gap 的殼走 rebuild**：body / form / collapse-wrap 在 Figma 退成非 component（rebuild 源），YAML 改 rebuild schema（`rebuild.frame` 畫殼 + **頂層 `slot`**、非 children）；base / main / main-with-step 清肚子 re-publish、仍 detach。判準：殼有無「底色 / 圓角 / padding 等免費樣式」值得 detach 保留——有＝detach、只有 gap＝rebuild。`_index` 標 `mode`
- **slot → 節點填充目標明確化（Q2）**：`content: list` 在 main 填進具名子 frame（`Content`）、在 body 填容器自己，差別過去藏著。detach 容器（main / main-with-step / collapse）補 `structure`（先用 MCP 讀真圖層、鏡射真實層級，標 `(fillable)` frame 與各 slot 所在層）；node-guide 明訂「slot → 節點解析」規則；template fillable 標記 `→ 見 slot` 統一成 `→ slot.<name>`；`lint.py` 加守門「detach 缺 structure → WARN」
- **optional 三機制併列**：結束狀態一致、執行分三種（detach hide／rebuild component create-hide／rebuild container 不建）；決策點補「fixed vs optional 是設計意圖、Figma 不一定看得出 → AI 提案（core=fixed、aux=optional、可參考 figma library component 的 `visible`）、不確定預設 fixed」
- **node-guide 結構整頓**：`slot` / `accepts` 是 container / template 共用，抽成 `### slot（container / template 共用）` 共用區（消掉埋在「detach 模式」下的 h5、修一批「指回 detach」的交叉引用）；Container（detach）只剩真正專屬的 `layout`
- **術語收斂（跨檔）**：detach 產出統一叫「圖層結構」（收掉「樹／棵」比喻、「骨架」只留 template 角色名）；拿掉「薄 / 厚殼」冗餘標籤（detach / rebuild 已能區分）；`omit` → 「不建」；「母版」→「figma library component」。涉 node-guide / spec-guide / plugin-prd / CLAUDE / audit-library
- **易讀性**：6 個 container 的 `content: list` 行加 inline 註記（detach「填進 structure 的 Content frame」／rebuild「填進本容器、無子 frame」），人眼掃 YAML 一眼看出差別
- **todo.md**：C-1 拆 a/b/c（已做）、C-4 改新 rebuild 流程、新增 C-6（form.title raw text node 應引用 library text style）/ C-7（Q2 已完成）
- **lint**：全程 `0 ERROR / 0 WARN`

## 2026-07-01

### e2e 第三輪（生成模式，成熟格式）+ container 空殼化根因

- **e2e 第三輪**：新增 `frames/image to frame03.yaml`（國泰世華信貸頁，與 frame02 同頁）；用已收斂的成熟 spec 格式生成，驗證三處落地——Device 一律 brace `"{Device}"`、optional 節點（Notification / Form title / help_text）不要就省略 key、綠連結 + 橘提醒段走 segments 分段上色（G500 / O500）。實地生到 Figma、截圖對照原圖一比一
- **根因盤出（→ 決策走「container 空殼化」路 1）**：Main / Body / Form 的 Figma 元件肚子塞了 sample component，但 YAML 寫空殼 → 導致 InputGroup 是 detach cascade 下來的（非文件說的 rebuild）、且深層 Field Set 的 Device 綁定在 detach 時掉
- **實證**：detach 後容器 frame 層的 layout 變數（Main Width / Form Gap / Card Padding / Card Min Height）**留得住**，只有深層 leaf 的 variant 綁定會掉 → 空殼代價小；leaf Device 用 spec brace + `setBoundVariable` 補（API 已實測可行）
- **spec-guide 矛盾待修**：「巢狀 component props 展開」範例的 `# field_set 不寫 → 沿用預設`，與「Props」的「bound variable 一律 brace」對 Field Set 打架（Field Set 含 bound-variable Device）→ 這是 frame03 spec 漏寫 field_set 的直接原因
- **todo.md**：新增「Container 空殼化」C-1～C-5（含根因與已驗證備忘）+「工具/環境」通知修正

## 2026-06-30

### CLAUDE.md 瘦身：authoring 規則下放 node-guide

- **判準**：CLAUDE.md ＝ 路由 + 跨任務憲法 + 主幹流程；只在某子任務內才需要的 authoring 細則下放到該細則的家（node-guide），此處留指標
- **Rules 7 條 → 5 條**：留憲法（done=commit / frame 名稱空白 / 先索取 URL）；下放「不省略中間層」「`spec_example` 只引用自身」「三種取用模式」到 node-guide（已是詳細的家）
- **檔名規則瘦身**：留 `.md` 命名 + 不回改歷史；node yaml 的 kebab(檔名)／snake(spec key) 理由併入 node-guide「name」，移除回指 CLAUDE 的 pointer
- node-guide 補：`spec_example`「只引用自身」正文落地、常見錯誤反例、kebab/snake 的 why

### 編輯保險：刪 / 改名概念時全 repo 搜尋（grep）

- **根因**：刪「rebuild.children 是 spec_example 例外」時只改眼前一處，漏了常見錯誤表與 rebuild 段共兩處——修了視窗內就宣告完成、沒掃全檔
- **新規則**（CLAUDE.md Rules）：刪 / 改名一個概念 / 術語 / 交叉引用時，先全 repo 搜尋（grep）被刪字串、確認無殘留再宣告完成；新增 / 改值 / 修錯字免（條件式、定點，非每次稽核）
- **補強**：/write-doc 的 SSoT 自查條收緊成「實際 grep、別用眼睛掃」
- **用詞統一**：3 處裸「grep」改「搜尋（grep）」（CLAUDE.md / write-doc / audit-glossary），設計師也讀得懂

### node-guide 去矛盾：rebuild.children + spec_example 只引用自身

- **rebuild.children**：移除錯誤的「屬 `spec_example` 例外」框架（它倆是不同欄位、無關）共 3 處；機制（ref 用各自 `component_key` import 成 instance）從 YAML 註解升為 Rule 正文，註解瘦成輕量示範
- **spec_example 只引用自身**：原句「不嵌入別的 component 名稱」與下方 `form` 範例（`input_group: {}`）自相矛盾；改白話「只寫自己的 props，子節點列名留空 `{}`、props 在各自 YAML」，body + 常見錯誤同步
- lint：`0 ERROR / 0 WARN`

## 2026-06-29

### bound variable doc SSoT 收斂（/write-doc 體檢）

- **盤出問題**：Device 一律 brace、不省略不寫死（+ createInstance 原因）這條 spec 撰寫規則，在 spec-guide / node-guide / glossary / design-token **重複定義 4 次**，將來改規則要 4 處同步（漂移溫床）
- **收斂**：SSoT 定在 `spec-guide.md`「Props」（唯一完整規則）；其餘 3 處改「定義本職 + 連結」——node-guide `bound_variable` 欄只留欄位語意 + lint 守門、glossary 回純術語定義、design-token 只描述變數，spec 寫法一律「見 spec-guide「Props」」
- grep 實證：「不可省略 / 不可寫死 / createInstance 不自帶」現只剩 spec-guide.md 一處
- lint：`0 ERROR / 0 WARN`

### bound variable 機制：Device 響應屬性一律寫 brace `"Device": "{Device}"`

- **根因**：spec 寫 `"Device": DESK` 會把 detach 繼承來的 `{Device}` variable 綁定用字面值取代（解綁）、釘死斷點，破壞 TB/MB 響應。8 個 component 的 `spec_example` 都在教這個錯（散播源）
- **通用三形式**（升格 spec-guide「Props」，適用所有 prop）：省略=延用（不發 setProperties）／`prop: value`=寫死（setProperties）／`prop: "{變數名}"`=主動綁（setBoundVariable）
- **新術語 `bound variable`**（glossary）：某 prop 該綁定的 Figma variables；node YAML 以 `bound_variable: "{Device}"` 標記，供人辨識「別寫死」與 `/audit-library` 守門
- **9 個 node YAML** 的 Device prop 補 `bound_variable: "{Device}"`；`{Device}` 登記進 design-token.md「Layout variables」表（lint 白名單，11 個變數）
- **關鍵修正——獨立引用 instance 不自帶綁定**：`createInstance()`（放進 slot / rebuild children 的元件，佔多數）不會帶 library 的 Device 綁定，故「省略」會得到未綁的預設 variant、不響應。定版規則：**bound variable prop 一律寫 brace 形式 `"Device": "{Device}"`**（form-3 → setBoundVariable）——不可省略、不可寫死；detach 繼承的雖已綁，一律 brace 是冪等重綁（無害）→ 不分路徑
- **全文對齊**：9 component spec_example 補 `"Device": "{Device}"`、node-guide / spec-guide（含完整 frame 範例 5 個響應元件、常見錯誤反例）/ design-token / glossary 措辭統一
- lint：`0 ERROR / 0 WARN`

## 2026-06-26

### 可選節點機制：`optional` 標記 + 統一「隱藏」執行

- **根因**：help_text 三層 boolean 全關只隱藏內部文字，instance 外殼仍有 26px 高，產出留空殼。本質是「整個節點要不要存在」的問題，不是 prop 層的開關——需要在「節點是否選用」這層處理
- **收斂成一條通則**：節點預設**必放**，只有少數**可選**的才標 `optional`（detach 與 rebuild 兩模式通用）；slot 詞彙沿用既有 `optional`（Form title 先例），不發明新機制
- **`optional` 標記**：`breadcrumbs` 從 `fixed` 改 `optional`（[main.yaml](containers/main.yaml) / [main-with-step.yaml](containers/main-with-step.yaml)）；[input-group.yaml](components/input-group.yaml) 的 Help Text child 加 `optional: true`
- **撰寫語意**：spec **不寫該區塊 = 隱藏**（auto-layout 不佔位）；**寫了即使內容全關 = 照放**（空殼是刻意的）。隱藏管「整個節點」，節點內部開關（如 help_text 三層 boolean）是另一層
- **執行統一為「隱藏（`visible=false`）」**：不刪除（保留結構、設計師可點回）；兩模式只差方向——detach 直接隱藏現成節點、rebuild create 後隱藏
- **文件**：[node-guide.md](node-guide.md) slot 段補三值表（fixed/optional/list）+ 兩模式執行說明、rebuild children `optional` 語意 + 範例；[spec-guide.md](spec-guide.md) 新增「可選節點（optional）」撰寫規則 + 執行模型補一行
- lint：`0 ERROR / 0 WARN`

## 2026-06-24

### design-token 補登 7 個常用 color style + 新增用途欄

- **盤點 library 色碼**：templates / containers / components 無「會生效的寫死色碼」；5 處 hex 皆為描述性註解（`用途` / `structure`），顏色實際由 library 元件內建、detach/instance 繼承——不需改
- **補登 6 個常用色**（key 全從 library `X6keMvwkHxhLu8ZWQnQgmi` 實抓，無猜測）：`Gray900` 文字黑、`Gray600` 可點擊文字/icon、`Gray100` Page bg、`Gray0` Container bg（白）、`B1000` Primary button、`R700` 檢核/錯誤紅（`Gray700` 已在表內）
- **White → `Gray0`**：CUBE 白色真名是 `Gray/Gray0`，依「短碼＝真名 `/` 後段」規則登記為 `Gray0`，不用 `White`（否則破壞短碼可機械推導）；同名陷阱：取純色 `Gray/Gray100`，非 `Opacity/Gray100`（半透明版）
- **登記表新增「用途」欄**：灰階 `Gray600/700/900` 光看短碼分不出語意，標上角色
- **重新定位該節**：開頭改述「此表服務『主動指定顏色』場景（分段上色為主，未來上色需求同理），多數元件色靠繼承、不經此表」

### design token 拆檔：layout variables + library color styles 獨立成 `design-token.md`

- **新檔 `design-token.md`**：把 node-guide.md 的「已知 variables」與「已知 library color styles」兩張登記表搬出，獨立成 design token 單一來源（Overview → Layout variables → Library color styles + segments 虛擬碼 → Appendix machine-read）。理由：登記資料 vs YAML 撰寫指南讀者 / 改動頻率不同，且 token 是會持續增列的 registry，獨立後各自演化
- **machine-read 同步**：`lint.py` 的 `load_known_vars` 讀取路徑 `node-guide.md` → `design-token.md`（docstring / 註解 / ERROR 訊息一併對齊）；白名單 13→10（`{id}`/`{key}`/`{name}` 留在 node-guide 散文、無 YAML 使用，不影響）
- **10 處 referrer 接線**：node-guide（讀法 / Variable 引用 / Props 格式）、spec-guide ×3、glossary、todo、audit-library SKILL ×3、write-doc SKILL machine-read 清單，全部改指 design-token.md
- lint：`0 ERROR / 0 WARN`

### audit-glossary「採用程序」：把術語採用定義成強制收尾清單

- **根因**：上一筆 commit 升格 `library color styles` 時只做了「定義進 glossary」一步，漏了「收斂呼叫點 / 砍重複定義」，自製 SSoT 違規 + 留下死連結。診斷出失誤不是「漏跑 skill」，而是「採用一個術語」其實是一套有固定收尾清單的動作，觸發點是「人確認」而非「跑了哪個 skill」
- **`audit-glossary/SKILL.md` step 5**：「逐一確認後採用」→「採用程序」。鎖在**人確認候選後才執行**、**入口無關**（手動加術語也適用）；把原本「可選：換措辭」升為**強制收斂呼叫點**，補上「源文件重複定義句 → 砍成連結（SSoT）」與「改名 → 更新 referrer 避免死連結」
- **`glossary.md` 新增規則**：補指針「採用不只是加一行，須照採用程序收尾」——因手動加術語的人讀的是 glossary 不是 skill，把兩個入口接到同一份程序



### 分段上色術語定案：library color styles 升格 glossary + 用詞統一

- **改用詞「paint style」→「library color styles」**：設計師不認得「paint style」，改用 Figma 介面原生詞「Color Styles」。spec-guide / node-guide / pre-action-note 全數對齊（含 node-guide Appendix 段標題「已知 paint styles」→「已知 library color styles」）
- **升格全域術語**：`library color styles` 進 `glossary.md`（術語 5→6），定義聚焦在非顯而易見的限制——**只能用 library 發佈的，不可用產出檔自建的 local color style**（後者不隨設計系統連動、跨檔取不到）；別名 `color styles`
- **修自製的 SSoT 違規**：升格後 node-guide「已知 library color styles」節原本重複了 glossary 的定義句，砍掉、改成連結；該節只留它獨有的「短碼↔key 登記表 + 取用機制」
- **清殘留漂移 + 死連結**：`todo.md` 兩處仍用舊詞「paint style」且指向已改名的 section，一併對齊
- **lint.py 修誤判**：variable 偵測 regex `\{([^}]+)\}` → `\{([^}:]+)\}`，排除冒號——CUBE variable 名不含 `:`，YAML inline map（`{ t: …, color: … }`）必含 `:`，舊 regex 把 segments 行誤報成未登記 variable
- lint：`0 ERROR / 0 WARN`

## 2026-06-23

### write-doc 戰術細則：新增「獨立引用測試」判準

- **磨利「列點/表格優先」**：把模糊的「單一線性思路才用散文（別硬拆）」換成可操作的**獨立引用測試**——「一支能不提另一支就單獨引用＝對等主張→拆清單（項數＝主張數）；一支只是另一支的例外/邊界＝單一主張＋條件→留散文」
- **與刪除測試形成序列**：刪除測試管「內容該不該存在」（存活軸）→ 獨立引用測試管「留下的排成清單還是散文」（排版軸）；同屬「寫完拿來自測」的動作測試家族，不新增第 5 條原則
- **Examples 補反例**：示範「摘要先行」不該硬拆成巢狀清單——「已自明別硬加」是邊界非對等項（1 主張＋條件），保留散文
- **自查清單「結構化」條**：補上獨立引用測試指引，讓自查有具體判準可跑

## 2026-06-22

### e2e 第二輪（生成模式）跑通 + 補「.key ≠ 已發佈」安全網

- e2e 第二輪「生成模式」走 detach 流跑通：import `AI/Template/Base` → detach → 以 `AI/Container/Main` 替換 Main with Step（無步驟頁）→ 客製 detach 後自帶的 body / form / pre_action_note / button_group scaffold，產出國泰世華信貸表單 frame（`image to frame 02`）於第一輪產出右方，保真度 OK
- 新增 frame spec `projects/AI 生成設計稿測試/frames/image to frame 02.yaml`：props key 改用 Figma 可讀名（對齊 node YAML 與 spec-guide），不再用第一輪的友善別名
- **抓到並修補「`.key` 存在 ≠ 已發佈」漏洞**：e2e 實測 `AI/Container/*`、`AI/Template/Base` 的 key 與 library 一致、Part B 全綠，卻 `importComponentByKeyAsync` 失敗——純粹未 publish。根因＝`.key` 在未發佈時就有值，抓到 key 不等於已發佈
- `audit-library` 新增 **Part C 發佈對照**（需非 library 探測檔）：Tier 1 從探測檔 import 驗是否真的發佈（COMPONENT / COMPONENT_SET 各用對的函式，失敗＝未發佈 ERROR）；Tier 2 比對已發佈版 vs 本地節點的結構指紋，偵測「改了忘記 re-publish」（WARN，僅抓結構性迭代，純視覺微調抓不到）；args 表 / 完成後回報 / 描述同步更新
- `node-guide.md` 的 `component_key` 加 caveat：未發佈也有 `.key`，發佈與否交給 `/audit-library` Part C 驗
- `todo.md`：新增兩筆 e2e 第二輪保真度問題（Input Group 空 Help Text 仍占高度；base detach 後 Header / Footer 的 variable 綁定遺失）＋ pre_action_note 富文字（綠連結／橘字無法以純字串保留）

## 2026-06-18

### 首輪 /audit-glossary：收斂 4 個重複概念為術語

- 跑 `/audit-glossary` 全 repo 盤點，採用 4 個術語（連種子共 5），措辭漂移收斂、跨檔一致
- **命名原則定案**（寫進 audit-glossary Rule + write-doc 戰術細則）：命名用**名詞、英文優先**（英文彆扭再用中文）、沿用既有詞軸
- 新增術語：`Pack component`（取代「未 publish 的單純/包裝 frame、如 Input Group」9 處）、`中間內容區域`（取代 中間區 / 中間內容區 / 頁面中間內容區 9 處）、`gap ladder`（取代 完形 gap 階梯 / 完形階梯；並把重複的 gap 值收進 glossary 當 SSoT，CLAUDE 改引用）、`可讀名`（prop 義的「真名」13+ 處）
- **「真名」overload 解決**：盤點發現 `可讀名` 本就一致、亂源是 `真名` 三義 → prop 可讀名一律 `可讀名`、完整 key `可讀名#id`、節點名留 `節點真名`；live 文件的 `真名` 現在只剩節點義
- 修回退：上次移除「葉」後，audit-glossary 例子又寫了「葉元件」，改回「元件」
- lint：**0 ERROR / 0 WARN**（5 術語全非孤兒；gap ladder 全域/區域衝突 WARN 靠收 CLAUDE 重複值清掉）

### 建立術語（glossary）機制

- 把 write-doc 的 SSoT 從「規則」延伸到「詞彙」：建立專案共同語言（像程式的全域 / 區域變數），集中定義、命名一致、可機器守門
- **scope 跟著 usage**：跨 md 的術語 → 全域 `glossary.md`；單檔術語 → 該檔 Model 段；區域詞擴散到第 2 檔再升級進 glossary
- **命名原則**：優先沿用既有詞軸（detach / instance / rebuild、container / component），避免撞名（如「Group component」會撞 `*_group`，不採用）
- 新增 `glossary.md`（全域術語單一來源；種子只放已是事實標準的 `繼承參考`，其餘走 audit-glossary 提案）
- 新增 `audit-glossary` skill（盤點重複概念 → 提案命名 / scope → 討論 → 採用；發現用 AI judgment，照 write-doc 6 段骨架寫）；與 `audit-library` 形成 `audit-*` 家族（library 機械 lint、glossary 判斷發現）
- `lint.py` 擴充 glossary 機械守門（經 `/audit-library`）：① 術語重複定義（ERROR）② 孤兒＝定義卻沒人用（WARN）③ 全域 / 區域衝突（WARN）
- write-doc 整合：戰術細則加「重複概念命名」、自查清單加「術語收斂」、情境 B 盤點納入 `/audit-glossary`、machine-read 保護清單加 `glossary.md`
- CLAUDE.md 參考表加 `glossary.md` / `/audit-glossary` 兩列
- lint：**0 ERROR / 0 WARN**（種子術語通過；故意注入重複 + 孤兒驗證守門生效後還原）

### 修正 spec-guide props key 約定漂移

- spec-guide.md 原寫「props key = Figma 真名，帶 `#id` 後綴（如 `"Text#5256:0"`）」與 node-guide.md 約定打架；node-guide 才是來源：spec 用**可讀名**（不帶 `#id`），id 另存在 node YAML 的 `id:` 欄，`可讀名#id` 由生成端（Stage B）呼叫 `setProperties` 時才組出
- 修三處：欄位規則（line 39）、常見錯誤 ✗/✓ 表（✓ 改 `"Text":`、✗ 多收「spec 帶後綴」）、Appendix 執行模型（setProperties 那步精確化為 `可讀名#id`）
- 釐清三層 props key 形式：frame spec＝可讀名、node YAML＝可讀名 + 另存 `id:`、IR / setProperties＝`可讀名#id`
- lint：**0 ERROR / 0 WARN**

### 依 write-doc 重寫 spec-guide.md

- `spec-guide.md` 套上 write-doc 的 6 段骨架（原為「核心概念 / 撰寫規則 / Frame Spec 格式 / 警示」四塊扁平堆疊 → Overview / Model / Workflow / Rule / Examples / Appendix）
- SSoT 收斂：「只寫需要覆蓋的 props」4 處 → 1 處（Rule ### Props 唯一解釋，他處連結或範例示範）；「層級對應圖層」收成「概念對應（Model 表）+ 不可跳層 directive（Rule）」兩維度；gap 階梯跨檔重複改連結（spec 本就不寫 gap）
- 互斥職責：AI 執行模型 code block 從概念段降到 Appendix；讀取順序（懶加載）從 Rule 抽到 Workflow
- 標題去前綴 / 括號（`核心概念：宣告式結構`、`讀取順序（懶加載）`、`警示標註規則`）；句中強調粗體降為純文字 / 標籤
- 新增「常見錯誤 ✗/✓」表（跳層、真名 vs 別名、同質欄位未包 form、props 寫太滿）
- 流程走 copy 沙盒（`spec-guide-copy.md` 重寫 → 確認後取代原檔），原檔零風險

### 移除「葉」術語

- `葉 component` / `葉元件` → `component` / `元件`（component 已定義為「有 props 無 slot 的內容」＝末端，「葉」屬冗字）
- `葉 instance` → `內層 instance`（detach 後仍連 library 的是內層 instance，比「葉」更貼切對比「外殼」）
- 涵蓋 CLAUDE.md / node-guide.md / plugin-prd.md / spec-guide.md / input-group.yaml 共 15 處；CHANGELOG 歷史保留原字面
- lint：**0 ERROR / 0 WARN**

## 2026-06-17

### 文件改名：node-format → node-guide、spec-rules → spec-guide

- 兩份框架文件改名，統一命名邏輯：**前綴 `node` / `spec` 分世界、後綴一致 `-guide`**（`format` 易誤會成排版；`rules` 與內文 Rule 段打架，且兩者皆含概念 / 流程 / 範例，`guide` 才涵蓋得住）
- `node-format.md` → `node-guide.md`（H1 改「Node YAML 撰寫指南」，對齊既有「Spec 撰寫指南」）
- `spec-rules.md` → `spec-guide.md`
- 全 repo ~24 處引用同步更新，含 `lint.py` 功能性 hardcode（`load_known_vars` 讀 `node-guide.md`）、CLAUDE 參考表 / 專案結構 / Rules、audit 與 write-doc 兩 SKILL、plugin-prd；CHANGELOG 歷史保留原名
- lint：**0 ERROR / 0 WARN**

### 新增 write-doc skill ＋ 依其重寫 node-format.md

- **新 skill `write-doc`**（`.claude/skills/write-doc/SKILL.md`）：框架文件撰寫規範，目標降低讀者（人 / AI）理解成本。含固定 6 段骨架（Overview / Model / Workflow / Rule / Examples / Appendix）、4 原則（概念流程規格分離、SSoT、先做法後理由、易理解＞易讀＞完整）、8 條戰術細則（摘要先行 / 標題只放標籤 / 反例條件式 / 粗體節制 / 刪除測試 / 列點表格優先 / 同主題單一來源…）、新增與調整兩情境程序
- **執行保證採散文層**：自查清單改「強制逐條輸出 ✓/✗」；反例與 SSoT 從打勾升級為「列易錯規則清單 / 建『事實→所在』對照」逼出漏洞；結構面用「互斥職責 + 同主題單一來源（按維度切）」讓重複無處可放
- **`node-format.md` 依 write-doc 全面重寫**：原 11 個平級 H2 → 6 段骨架；行動優先（「為何不能跨檔複製 / 為什麼有 id / detach 機制」移 Appendix）；新增「常見錯誤 ✗/✓」表；detach 段由 5 條+巢狀瘦身為 2 條 actionable + 比較表；粗體歸零；標題砍掉限定詞括號（保留消歧義）；SSoT 按維度切（必填/模式歸欄位順序、語意歸欄位說明）；修正標題 / 開頭「漏 Template」漂移
- lint：**0 ERROR / 0 WARN**

## 2026-06-16

### 命名規則建立 ＋ node 名一律英文 ＋ 文件檔名統一

- **node 三名一致規則**（`name` / 檔名 / spec key 由 Figma 真名單一推導）寫進 `node-format.md` 的 `### name`：`name` = 真名原樣大小寫、檔名 = `kebab(name)`、spec_example 根 key = `snake(name)`；`/audit-library` 離線 lint 強制檢查（新增 `check_naming`：檔名 = `kebab(slug)`、spec 根 key 字面 = `snake(slug)`）
- **修齊既有不一致**：container `name` 補大寫（`main → Main`、`body → Body`、`main with step → Main with Step`）、template `name` 補大寫（`base/result/intro/modal → Base/Result/Intro/Modal`）、spec key 空格→底線（`main with step:` → `main_with_step:`）；`_index` / `spec-rules` 同步
- **node 名一律用英文**：遇中文元件請設計師在 Figma 改英文真名；`aka` 降為「過渡橋接」，lint 對中文 `name` 發 WARN。設計師已把 `Input Group 驗證碼` 改為 `Input Group Verification`，YAML / `_index` / `form.accepts` 同步、移除 `aka`
- **文件檔名統一**：`Plugin-PRD.md → plugin-prd.md`（`.md` 一律小寫 kebab，`CLAUDE.md` / `CHANGELOG.md` 大寫例外）；「檔名規則」濃縮寫進 `CLAUDE.md` Rules（含 kebab vs snake 理由）
- lint：**0 ERROR / 0 WARN**

### Template 納入 node-format ＋ 4 大 template 依真實圖層重推

- **node-format.md 新增 Template 格式**：template（整頁骨架）走 detach 模式，YAML 必須以 `structure` **如實鏡射 Figma 圖層樹**（固定 instance + 中間內容區，標 frame/instance 性質）+ `slot` + `spec_example`；不可臆測欄位（修正 intro 過去憑空編 heading/steps/buttons 的問題）
- **base / result / modal / intro 依真實結構重推**（use_figma 核對）：base = Header / Main with Step / Footer（Figma 端已移除隱藏 Modal 層）；result = Header / Main（NPS 橫幅 / Breadcrumbs / Content）/ Footer；modal = Modal Head / Contents / Modal Footer；intro = Header / Intro with content（instance，component 待補）/ Footer
- **intro 已 publish**（node_id `11031:46694`、key `be4333b5…`）；**base 拼字修正** AI/Tepmlate → AI/Template（key 不變）
- **detach 深度規則**：template 中間區是 frame → 一次 detach 可編輯；是 instance（intro 的 Intro with content）→ 需設 props 或再 detach。**無步驟頁面用 `main` 容器**（不可隱藏 State Steps）
- **template 納入 lint/audit**：改用 `spec_example` 後自動受 lint 檢查；audit Part B 新增「template/container 結構 ↔ Figma 子層樹」對照
- 待補 component：Intro with content、Announcement NPS（之後補）
- lint：**0 ERROR / 0 WARN**

### GroupLayout 改名為 Field Set ＋ commit 流程調整

- **GroupLayout → Field Set**（spec key 由擠成一團的 `grouplayout` 變為 `field_set`）：新增 `components/field-set.yaml`（刪 `group-layout.yaml`），node_id / component_key / props 皆不變；用途改寫為「一到多個相關輸入欄位排成一組，如電話 區碼/主碼/分機（3-2 變體）」；全 repo 引用更新（input-group rebuild、input-group-verification、form accepts、`_index`、node-format、spec-rules、todo）。Figma 端已同步改名（key 不變，三者對齊）
- **CLAUDE.md「done」規則調整**：改為直接 commit + push（不需先確認 message），push 後回報 commit 內容；co-author 更正為 `Claude Opus 4.8`

### help-text props 改名對齊（drift 解除）

- 設計師於 Figma 重新命名 help-text props 並重 publish：bool 加 `Show` 前綴（`Show 警示文字 / Show 橘色文字 / Show 灰色文字`）、text 統一 `…內容`（`警示內容 / 橘字內容 / 灰字內容`），語意清楚
- `components/help-text.yaml` 同步真名（key/id 不變），移除原本的命名混亂 ⚠️ 與 drift 警告；連帶更新 `input-group.yaml` 引用；`todo.md` drift 項標為已解
- lint 仍 0 ERROR / 1 WARN（intro 待 publish）

### Round 2：節點 YAML 全面套用 detach 流格式 + props 改 Figma 真名（可讀名 + id）

- **components（16）**：props 全改 Figma 真名，採「**可讀名當 key + `id` 另存**」格式（VARIANT 無 id，生成時組回 `名#id` 餵 setProperties）；補 `component_key`（由 node_id 抓 `.key`）；button-group / notification 等無頂層 property 的值改記 `nested_overrides`；**input-group 改為 rebuild 模式**（Label / GroupLayout / Help Text）
- **containers（6）+ templates**：改 detach 模式（`component_key` + `detach: true`），node_id 移至已 publish 的 `11018:*`，`layout` 標「繼承參考」；**base-page 改名為 base**（刪舊檔）；result / modal 補 key，intro 留待補
- **node-format.md**：新增「為什麼屬性有 id」的 Figma 機制說明；props 格式定為「可讀名 key + `id` 欄」（有 id=property、無 id=VARIANT、附撞名例外規則）
- `_index.yaml`（components / containers）補 `component_key`；`lint.py` 加三模式檢查（key 待補→WARN、rebuild.children.ref 驗證）+ nested_overrides 辨識；spec-rules / todo 同步
- `/audit-library` Part A：**0 ERROR / 1 WARN**（僅 intro key 待補）
- 待辦（todo.md）：intro publish、help-text 重 publish 對齊改名、GroupLayout 建議改名「Group Layout」、base 的 Figma 名 Tepmlate 拼字

### 導入 detach 流：跨檔取用 library 的三種模式（Round 1 — 框架/格式/流程文件）

- e2e 實測發現 **Figma Plugin API 不能跨檔複製 frame**，CLAUDE.md 舊寫的「從 library 複製範本 frame」做不到；已驗證解法為 **detach 流**（import published component → `createInstance` → `detachInstance()` **一次**，得保真度 100% 可編輯骨架，淺層 detach 使內層 frame 一次全可編輯、葉 instance 與 variable 綁定保留）
- `node-format.md` 定義**三種取用模式**：**detach**（template/container，`component_key` + `detach: true`）、**instance**（葉 component，`component_key` + props）、**rebuild**（未 publish 的包裝 frame 如 Input Group，照 `rebuild` 重畫）；新增 `component_key` / `detach` 欄位、`nested_overrides`（無頂層 prop 的值，如 button 主按鈕文字）；props 改用 **Figma 真名**（難懂者 `⚠️` 建議改名 + `description`）；容器 `layout` 降為「繼承參考」
- `CLAUDE.md` / `spec-rules.md`：生成流程與執行模型改為 import(+detach/rebuild)，明訂「只在最外層 detach 一次、內層免 detach、由外往內為製作順序」；聲明 detach/rebuild 只改執行、不改 spec 撰寫
- `Plugin-PRD.md`：IR 節點加 `mode`（detach/instance/rebuild），`variable→id` registry 因 detach 繼承大幅縮小，prop registry 內嵌為各節點真名
- `/audit-library`：`lint.py` 加三模式欄位檢查（`component_key` 待補 → WARN、`rebuild.children.ref` 驗證）；`SKILL.md` Part B 改比對 Figma 真名（lint 0 ERROR / 25 WARN）
- `todo.md` 新增 **Round 2** 區塊：~28 個節點 YAML 改寫成新格式（補 key、detach、真名 props、Input Group rebuild），待使用者 publish template/container 後執行
- 新增 `enhancement.md`（e2e 踩雷 P1–P4 + 優化 O1–O5）；e2e 產出 `projects/AI 生成設計稿測試/`（國泰世華線上申請信用貸款表單頁，催生本次 detach 流改版）

## 2026-06-15

### 規劃 Stage B 編譯器（spec.yaml → Figma frame 純腳本化）

- 釐清流程兩段：**(A) 意圖 → spec.yaml** 需 AI 判斷；**(B) spec.yaml → Figma frame** 本質是確定性編譯，可離線腳本化（Figma Plugin API），不需 AI
- 新增 `Plugin-PRD.md`：背景動機、現況 MCP `use_figma` 經 AI 層的不一致問題、目標架構（spec → render-plan.json IR → Figma plugin）、前提 registry（node_id→component key、prop 真實屬性名/type、variable→id）、風險與 B-0~B-4 任務細節
- `todo.md` 新增「Stage B 編譯器」區塊：壓成 B-0~B-4 各一行條目，blocked 待 e2e 走順、spec 格式穩定才解鎖；細節指向 `Plugin-PRD.md`

## 2026-06-12

### 補齊 Form/Collapse Wrap/Collapse 容器,variable 引用語法通用化

- 容器補齊 node_id：Form(`10992:10640`)、Collapse Wrap(`10992:10687`)、Collapse(`10996:11440`)
- Collapse 抽成獨立容器(白底邊框卡片:Collapse Header + 可收合內容區);`collapse-wrap` 改為引用 `collapse` 真實節點,移除原本的 inline 偽建模
- **variable 引用語法通用化**：`"{Variable Name}"` 不再只用於 `width`,凡 `gap` / `padding` 綁定 Figma variable 者一律比照;`node-format.md` 新增「Variable 引用」段落(判斷方式 + 正式名用 `get_variable_defs` 查),變數表擴充為 12 個並分寬度／間距兩類
- 套用真實變數名：`form` gap `{Form Gap}`、`collapse-wrap` gap `{Collapse Wrap Gap}`、`collapse` 內容區 `{Form Gap}` / `{Card Padding}` / `{Collapse Bottom Padding}`;`main`(40)、`body`(24) 經查證為字面值維持不變
- `/audit-library` 的「已知 variable」白名單即此表,變數改名／拼錯會被 lint 抓出(本次 12 個全通過)

### 補齊容器、修正元件 props,新增 /audit-library 一致性盤點 skill

- 容器層：`card` → `body` 改名並補真實 node_id `10992:10570`(gap 24、width fill、notification 選填 + content);`main` / `main with step` 補 node_id 與 `last_verified`,spec 如實寫出原本跳過的 `body` 巢狀層;`main` 補 `breadcrumbs` fixed slot
- 元件修正(對照 Figma 真實 props)：State Steps 廢除自創的 `total/current/labels`,改用真 prop `Stpes`("N Steps M") + `step1`~`step5`;`breadcrumbs.visible`(捏造)→ 真 prop `textLink`;`upload-group` spec_example 舊格式 `component:/props:` → snake key;`input-group-verification` spec key 對齊 Figma 真名「Input Group 驗證碼」
- 新增 `/audit-library` skill(`.claude/skills/`)：`lint.py` 離線掃 library 命名/props/variable 內部一致性(per-component 不混淆,範圍不含 frames);`SKILL.md` 定義 Part A 離線 lint + Part B 用 node_id 回 Figma 偵測改名,並規定 prop 改名須限縮在該節點脈絡、不可全域取代
- 警示表收斂為「library 文件不完整」三條;frame 由生成時用當下名稱保證一致,故 audit 不掃 frames
- `CLAUDE.md` 新增規則：如實巢狀、spec_example 只引用自身、登記 `/audit-library` skill

### 新增 Container 容器層架構

- 在 `components/` 與 `templates/` 之間建立第三層 `containers/`（排版殼，有 slot）
- 新增 5 個容器 YAML：`main`（gap 40）、`main-with-step`（gap 40）、`form`（gap 20）、`card`（gap 24）、`collapse-wrap`（gap 32）
- `templates/main.yaml` 拆成兩個獨立容器，原 variant 機制廢除；`templates/base-page.yaml` 改用容器 key
- `component-format.md` 整合為 `node-format.md`，統一 component 與 container 的撰寫格式
- `CLAUDE.md` 新增「Container 使用判斷邏輯」：完形 gap 階梯（main 40 → Collapse Wrap 32 → Card 24 → Form 20）、≥2 同質表單欄位必須包進 Form 等規則
- `spec-rules.md` 更新 key 性質辨識表、gap 階梯說明、frame spec 範例改為 form 包裝版本
- Form / Card / Collapse Wrap 的 node_id 待補（使用者將提供 Figma 基底節點 URL）

---

## 2026-06-08

### Component YAML 批次補齊

- 用 6 個並行 sub-agent 從 Figma MCP 補齊 props：data-list-row、group-layout、pre-action-note（原 personal-data-protection-default）、illustration-and-text、notification、upload-group
- table-cell、missing-component 暫 pass（node_id 待補）
- 更新 `todo.md`，標記上述 6 個為完成

### Pre Action Note 元件同步

- Figma library 元件由「PersonalDataProtection/Default」改名為「Pre Action Note」
- 新增 `text` prop：選填，傳入時取代預設個資聲明，內容格式不限
- 檔案由 `components/personal-data-protection-default.yaml` 改名為 `components/pre-action-note.yaml`
- `_index.yaml` 同步更新名稱與用途說明

### 寬度排版系統

- 設計並實作 `width` 欄位，值域：`fill`（填滿父容器）或 `"{Variable Name}"`（Figma Variable 固定寬度）
- `component-format.md`：加入 `width` 欄位說明、`{...}` variable 語法、已知 layout variables 表格（Page Width / Main Width / Card Grid 10col）
- `spec-rules.md`：新增寬度規則段落，說明 fill 不寫寬度、variable 同名帶入、只生成 DESK 稿、容器層級圖
- 全部 16 個 component YAML 批次加入 `width: fill`

---

## 2026-05-20

- 建立專案初始結構（CLAUDE.md、projects/、todo.md）
- 定義 agent 角色、生成／修改模式流程、Component 使用判斷邏輯
- 補齊 6 個 template 的 node_id（step、no-step、collapse-wrap、result、modal s、intro）
- 補齊 12 個 component 的 node_id（Header ～ Upload Group）
- 將 library 索引與 spec 格式從 CLAUDE.md 拆分為獨立檔案（library.md、spec.md）
- 將檔案格式從 Markdown 改為 YAML，重組為 templates/ 和 components/ 目錄結構
- 刪除 library.md 與 spec.md，CLAUDE.md 改為參照各 YAML 檔
- 將 step、no-step、collapse-wrap 三個 template 合併為 base-page，以 has_steps 和 content_layout 控制變體
- 更新 result、modal node_id，補齊所有 template 的 spec（result、modal、intro）
- 修正 result spec 結構（補 main 層級、欄位名稱對齊 component name）
- 重寫 base-page spec（對齊新規則：main 層級、欄位名稱對應 component name）
- 將 main 拆為獨立 template（main-state-step、main-no-state-step），base-page spec 的 main 改為空引用
- 將 main-state-step 與 main-no-state-step 合併為單一 main.yaml，以 variants 區分
- Rules 補入三條：spec 欄位名稱對齊 component、spec 層級對應 frame 層級、隱藏圖層不可見
