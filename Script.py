-- VersaTools Roblox Hub - Versão 3.3 (Modificado - Aimbot Corrigido)
local Players = game:GetService("Players")
local TweenService = game:GetService("TweenService")
local UserInputService = game:GetService("UserInputService")
local Debris = game:GetService("Debris")
local RunService = game:GetService("RunService")
local Workspace = game:GetService("Workspace")

local Player = Players.LocalPlayer
local PlayerGui = Player:WaitForChild("PlayerGui")
local Camera = Workspace.CurrentCamera

-- Remover hub anterior, se houver
if PlayerGui:FindFirstChild("VersaToolsHub") then
    PlayerGui:FindFirstChild("VersaToolsHub"):Destroy()
end

--[[============================================================
    CONFIGURAÇÕES DE TEMA E ANIMAÇÃO (Neon Rider Theme)
============================================================]]--
local Theme = {
    Background = Color3.fromRGB(20, 18, 26),
    Primary = Color3.fromRGB(30, 27, 40),
    Secondary = Color3.fromRGB(42, 38, 55),
    Accent = Color3.fromRGB(236, 72, 153), -- Hot Pink/Magenta
    AccentHover = Color3.fromRGB(255, 100, 175),
    Text = Color3.fromRGB(235, 235, 245),
    TextSecondary = Color3.fromRGB(160, 150, 180),
    Success = Color3.fromRGB(22, 163, 74),   -- Green
    Warning = Color3.fromRGB(252, 211, 77),  -- Yellow
    Error = Color3.fromRGB(239, 68, 68),     -- Red
    Stroke = Color3.fromRGB(60, 55, 80)
}

local AnimationInfo = {
    Fast = TweenInfo.new(0.2, Enum.EasingStyle.Quint, Enum.EasingDirection.Out),
    Medium = TweenInfo.new(0.25, Enum.EasingStyle.Quint, Enum.EasingDirection.Out),
    Slow = TweenInfo.new(1.5, Enum.EasingStyle.Sine, Enum.EasingDirection.InOut)
}

--[[============================================================
    VARIÁVEIS E LISTA DE SCRIPTS
============================================================]]--
local HubVisible = false
local ActivePage = nil

-- Variáveis de controle do Aimbot (CORRIGIDO)
local aimbotEnabled = false
local aimbotTeamCheck = false
local aimbotWallCheck = false
local aimbotTargetPart = "Head"  -- Variável central para a parte alvo
local aimbotPrediction = 0.15  -- Prediction em segundos
local aimbotFovRadius = 150
local aimbotShowFov = false
local aimbotSmoothingFactor = 0.5
local currentAimbotTarget = nil 
local aimbotActivationKey = "Mouse2"
local aimbotMode = "Câmera"
local mouseAimbotStrength = 10

-- NOVO: Sistema de Silent Aim
local silentAimEnabled = false
local silentAimHitChance = 100  -- Porcentagem de chance de acerto (0-100)

-- NOVO: Sistema de Amigos
local friendsList = {}  -- Tabela para armazenar amigos {[playerName] = true}
local nearbyPlayersUI = {}  -- Referências para UI dos jogadores próximos
local proximityRadius = 100  -- Raio para detectar jogadores próximos

local Scripts = {
    {"Orca", "https://raw.githubusercontent.com/richie0866/orca/master/public/snapshot.lua"},
    {"Velocity Car", "https://raw.githubusercontent.com/Documantation12/Universal-Vehicle-Script/main/Main.lua"},
    {"Farm Westbound", "https://raw.githubusercontent.com/ytnixks/Scripts-WORKING/refs/heads/main/westbound%202"},
    {"WestBound Script", "https://raw.githubusercontent.com/Sebiy/WestWare/main/WestWareScript.lua"},
    {"Hamburg Script", "https://vortex-hub.pages.dev/api/vortex"},
    {"Infinite Yield", "https://raw.githubusercontent.com/EdgeIY/infiniteyield/master/source"},
    {"Aimbot Pobreza", "https://pastebin.com/raw/WufDtFxj"},
    {"Aimbot Universal", "https://ayato-ware.vercel.app/Main.lua"},
    {"Endem Script", "https://raw.githubusercontent.com/MrEye12/BlackAir/refs/heads/main/Load%20System"},
    {"Animações Hub", "https://raw.githubusercontent.com/ocfi/aqua-hub-is-a-skid-lol/refs/heads/main/animatrix"}
}

--[[============================================================
    CRIAÇÃO DA INTERFACE (UI)
============================================================]]--
local ScreenGui = Instance.new("ScreenGui")
ScreenGui.Name = "VersaToolsHub"
ScreenGui.ResetOnSpawn = false
ScreenGui.Parent = PlayerGui

-- Frame Principal
local MainFrame = Instance.new("Frame")
MainFrame.Size = UDim2.new(0, 800, 0, 500)
MainFrame.Position = UDim2.new(0.5, -400, 0.5, -250)
MainFrame.BackgroundColor3 = Theme.Background
MainFrame.Visible = false
MainFrame.BorderSizePixel = 0
MainFrame.Active = true
MainFrame.Draggable = true
MainFrame.ClipsDescendants = true
MainFrame.Parent = ScreenGui

local MainCorner = Instance.new("UICorner", MainFrame)
MainCorner.CornerRadius = UDim.new(0, 12)
local MainStroke = Instance.new("UIStroke", MainFrame)
MainStroke.Color = Theme.Stroke
MainStroke.Thickness = 1.5

local MainShadow = Instance.new("ImageLabel", MainFrame)
MainShadow.Image = "rbxassetid://10368303214"
MainShadow.ImageColor3 = Color3.new(0, 0, 0)
MainShadow.ImageTransparency = 0.7
MainShadow.ScaleType = Enum.ScaleType.Slice
MainShadow.SliceCenter = Rect.new(49, 49, 50, 50)
MainShadow.Size = UDim2.new(1, 10, 1, 10)
MainShadow.Position = UDim2.new(0.5, -5, 0.5, -5)
MainShadow.AnchorPoint = Vector2.new(0.5, 0.5)
MainShadow.ZIndex = -1

local Header = Instance.new("Frame", MainFrame)
Header.Size = UDim2.new(1, 0, 0, 55)
Header.BackgroundColor3 = Theme.Primary
Header.BorderSizePixel = 0
local HeaderCorner = Instance.new("UICorner", Header)
HeaderCorner.CornerRadius = UDim.new(0, 12)
local HeaderGradient = Instance.new("UIGradient", Header)
HeaderGradient.Color = ColorSequence.new({ColorSequenceKeypoint.new(0, Color3.fromRGB(50, 45, 70)), ColorSequenceKeypoint.new(1, Theme.Primary)})
HeaderGradient.Rotation = 90

local HeaderLine = Instance.new("Frame", Header)
HeaderLine.Size = UDim2.new(1, 0, 0, 2)
HeaderLine.Position = UDim2.new(0, 0, 1, -2)
HeaderLine.BackgroundColor3 = Theme.Accent
HeaderLine.BorderSizePixel = 0
local LineGradient = Instance.new("UIGradient", HeaderLine)
LineGradient.Color = ColorSequence.new({ColorSequenceKeypoint.new(0, Theme.Accent), ColorSequenceKeypoint.new(1, Color3.fromRGB(150, 40, 100))})

local Title = Instance.new("TextLabel", Header)
Title.Text = "VERSATOOLS"
Title.Size = UDim2.new(1, -100, 1, 0)
Title.Position = UDim2.new(0, 25, 0, 0)
Title.BackgroundTransparency = 1
Title.Font = Enum.Font.Michroma
Title.TextColor3 = Theme.Text
Title.TextSize = 24
Title.TextXAlignment = Enum.TextXAlignment.Left
local TitleGradient = Instance.new("UIGradient", Title)
TitleGradient.Color = ColorSequence.new({ColorSequenceKeypoint.new(0, Theme.AccentHover), ColorSequenceKeypoint.new(1, Theme.Accent)})

local CloseButton = Instance.new("TextButton", Header)
CloseButton.Text = "X"
CloseButton.Size = UDim2.new(0, 35, 0, 35)
CloseButton.Position = UDim2.new(1, -45, 0.5, -17.5)
CloseButton.BackgroundColor3 = Theme.Primary
CloseButton.Font = Enum.Font.SourceSansBold
CloseButton.TextColor3 = Theme.TextSecondary
CloseButton.TextSize = 18
CloseButton.BorderSizePixel = 0
local CloseCorner = Instance.new("UICorner", CloseButton)
CloseCorner.CornerRadius = UDim.new(0, 8)

local Sidebar = Instance.new("Frame", MainFrame)
Sidebar.Size = UDim2.new(0, 180, 1, -55)
Sidebar.Position = UDim2.new(0, 0, 0, 55)
Sidebar.BackgroundColor3 = Theme.Primary
Sidebar.BorderSizePixel = 0

local SelectionIndicator = Instance.new("Frame", Sidebar)
SelectionIndicator.Size = UDim2.new(0, 4, 0, 40)
SelectionIndicator.BackgroundColor3 = Theme.Accent
SelectionIndicator.BorderSizePixel = 0
SelectionIndicator.ZIndex = 3
local IndicatorCorner = Instance.new("UICorner", SelectionIndicator)
IndicatorCorner.CornerRadius = UDim.new(1, 0)

local ContentFrame = Instance.new("Frame", MainFrame)
ContentFrame.Size = UDim2.new(1, -180, 1, -55)
ContentFrame.Position = UDim2.new(0, 180, 0, 55)
ContentFrame.BackgroundTransparency = 1

local DashboardPage = Instance.new("Frame", ContentFrame)
DashboardPage.Name = "DashboardPage"
DashboardPage.Size = UDim2.new(1, 0, 1, 0)
DashboardPage.BackgroundTransparency = 1
DashboardPage.Visible = false

local ScriptsPage = Instance.new("ScrollingFrame", ContentFrame)
ScriptsPage.Name = "ScriptsPage"
ScriptsPage.Size = UDim2.new(1, 0, 1, 0)
ScriptsPage.BackgroundTransparency = 1
ScriptsPage.ScrollBarThickness = 6
ScriptsPage.ScrollBarImageColor3 = Theme.Accent
ScriptsPage.BorderSizePixel = 0
ScriptsPage.Visible = false

local ESPPage = Instance.new("Frame", ContentFrame)
ESPPage.Name = "ESPPage"
ESPPage.Size = UDim2.new(1, 0, 1, 0)
ESPPage.BackgroundTransparency = 1
ESPPage.Visible = false

local AimbotPage = Instance.new("ScrollingFrame", ContentFrame)
AimbotPage.Name = "AimbotPage"
AimbotPage.Size = UDim2.new(1, 0, 1, 0)
AimbotPage.BackgroundTransparency = 1
AimbotPage.ScrollBarThickness = 6
AimbotPage.ScrollBarImageColor3 = Theme.Accent
AimbotPage.BorderSizePixel = 0
AimbotPage.Visible = false
local AimbotPageLayout = Instance.new("UIListLayout", AimbotPage)
AimbotPageLayout.Padding = UDim.new(0, 15)
AimbotPageLayout.SortOrder = Enum.SortOrder.LayoutOrder
local AimbotPagePadding = Instance.new("UIPadding", AimbotPage)
AimbotPagePadding.PaddingTop = UDim.new(0, 20)
AimbotPagePadding.PaddingLeft = UDim.new(0, 20)
AimbotPagePadding.PaddingRight = UDim.new(0, 20)
AimbotPagePadding.PaddingBottom = UDim.new(0, 20)

-- NOVO: Página Diversos
local DiversosPage = Instance.new("Frame", ContentFrame)
DiversosPage.Name = "DiversosPage"
DiversosPage.Size = UDim2.new(1, 0, 1, 0)
DiversosPage.BackgroundTransparency = 1
DiversosPage.Visible = false

local AllPages = {DashboardPage, ScriptsPage, ESPPage, AimbotPage, DiversosPage}

AimbotPageLayout:GetPropertyChangedSignal("AbsoluteContentSize"):Connect(function()
    AimbotPage.CanvasSize = UDim2.new(0, 0, 0, AimbotPageLayout.AbsoluteContentSize.Y + AimbotPagePadding.PaddingBottom.Offset)
end)

local WelcomeText = Instance.new("TextLabel", DashboardPage)
WelcomeText.RichText = true
WelcomeText.Text = string.format("Bem-vindo ao <b><font color='#%s'>VersaTools Hub!</font></b>\n\nVersão: 3.3 (Modificado)\nScripts: %d disponíveis\n\n<b>Controles:</b>\n• H - Abrir/Fechar Hub\n• V - Ativar/Desativar Aimbot\n• Arrastar para mover\n• X - Fechar", Theme.Accent:ToHex(), #Scripts)
WelcomeText.Size = UDim2.new(1, -40, 1, -40)
WelcomeText.Position = UDim2.new(0, 20, 0, 20)
WelcomeText.BackgroundTransparency = 1
WelcomeText.Font = Enum.Font.SourceSans
WelcomeText.TextColor3 = Theme.Text
WelcomeText.TextSize = 18
WelcomeText.TextXAlignment = Enum.TextXAlignment.Left
WelcomeText.TextYAlignment = Enum.TextYAlignment.Top
WelcomeText.TextWrapped = true

local ScriptsListLayout = Instance.new("UIListLayout", ScriptsPage)
ScriptsListLayout.Padding = UDim.new(0, 10)
ScriptsListLayout.SortOrder = Enum.SortOrder.LayoutOrder
local ScriptsPadding = Instance.new("UIPadding", ScriptsPage)
ScriptsPadding.PaddingTop = UDim.new(0, 20)
ScriptsPadding.PaddingLeft = UDim.new(0, 20)
ScriptsPadding.PaddingRight = UDim.new(0, 20)

local ESPTitle = Instance.new("TextLabel", ESPPage)
ESPTitle.Text = "Sistema ESP"
ESPTitle.Size = UDim2.new(1, -40, 0, 40)
ESPTitle.Position = UDim2.new(0, 20, 0, 20)
ESPTitle.BackgroundTransparency = 1
ESPTitle.Font = Enum.Font.SourceSansSemibold
ESPTitle.TextColor3 = Theme.Accent
ESPTitle.TextSize = 24
ESPTitle.TextXAlignment = Enum.TextXAlignment.Left

local ESPDesc = Instance.new("TextLabel", ESPPage)
ESPDesc.Text = "Mostra informações visuais dos jogadores através de objetos."
ESPDesc.Size = UDim2.new(1, -40, 0, 30)
ESPDesc.Position = UDim2.new(0, 20, 0, 60)
ESPDesc.BackgroundTransparency = 1
ESPDesc.Font = Enum.Font.SourceSans
ESPDesc.TextColor3 = Theme.TextSecondary
ESPDesc.TextSize = 16
ESPDesc.TextXAlignment = Enum.TextXAlignment.Left

local ESPToggle = Instance.new("TextButton", ESPPage)
ESPToggle.Text = "ESP: DESATIVADO"
ESPToggle.Size = UDim2.new(0, 200, 0, 50)
ESPToggle.Position = UDim2.new(0, 20, 0, 110)
ESPToggle.BackgroundColor3 = Theme.Error
ESPToggle.Font = Enum.Font.SourceSansBold
ESPToggle.TextColor3 = Theme.Text
ESPToggle.TextSize = 16
local ESPToggleCorner = Instance.new("UICorner", ESPToggle)
ESPToggleCorner.CornerRadius = UDim.new(0, 8)
local ESPToggleStroke = Instance.new("UIStroke", ESPToggle)
ESPToggleStroke.Color = Theme.Stroke
ESPToggleStroke.Thickness = 1

-- NOVO: Toggle para mostrar distância
local ESPDistanceToggle = Instance.new("TextButton", ESPPage)
ESPDistanceToggle.Text = "Mostrar Distância: NÃO"
ESPDistanceToggle.Size = UDim2.new(0, 200, 0, 50)
ESPDistanceToggle.Position = UDim2.new(0, 240, 0, 110)
ESPDistanceToggle.BackgroundColor3 = Theme.Error
ESPDistanceToggle.Font = Enum.Font.SourceSansBold
ESPDistanceToggle.TextColor3 = Theme.Text
ESPDistanceToggle.TextSize = 16
local ESPDistToggleCorner = Instance.new("UICorner", ESPDistanceToggle)
ESPDistToggleCorner.CornerRadius = UDim.new(0, 8)
local ESPDistToggleStroke = Instance.new("UIStroke", ESPDistanceToggle)
ESPDistToggleStroke.Color = Theme.Stroke
ESPDistToggleStroke.Thickness = 1

-- NOVO: Toggle para mostrar contorno (Highlight)
local HighlightToggle = Instance.new("TextButton", ESPPage)
HighlightToggle.Text = "Contorno: DESATIVADO"
HighlightToggle.Size = UDim2.new(0, 200, 0, 50)
HighlightToggle.Position = UDim2.new(0, 460, 0, 110)
HighlightToggle.BackgroundColor3 = Theme.Error
HighlightToggle.Font = Enum.Font.SourceSansBold
HighlightToggle.TextColor3 = Theme.Text
HighlightToggle.TextSize = 16
local HighlightToggleCorner = Instance.new("UICorner", HighlightToggle)
HighlightToggleCorner.CornerRadius = UDim.new(0, 8)
local HighlightToggleStroke = Instance.new("UIStroke", HighlightToggle)
HighlightToggleStroke.Color = Theme.Stroke
HighlightToggleStroke.Thickness = 1

-- NOVO: Toggle para verificar times
local TeamCheckToggle = Instance.new("TextButton", ESPPage)
TeamCheckToggle.Text = "Verificar Times: NÃO"
TeamCheckToggle.Size = UDim2.new(0, 200, 0, 50)
TeamCheckToggle.Position = UDim2.new(0, 680, 0, 110)
TeamCheckToggle.BackgroundColor3 = Theme.Error
TeamCheckToggle.Font = Enum.Font.SourceSansBold
TeamCheckToggle.TextColor3 = Theme.Text
TeamCheckToggle.TextSize = 16
local TeamCheckToggleCorner = Instance.new("UICorner", TeamCheckToggle)
TeamCheckToggleCorner.CornerRadius = UDim.new(0, 8)
local TeamCheckToggleStroke = Instance.new("UIStroke", TeamCheckToggle)
TeamCheckToggleStroke.Color = Theme.Stroke
TeamCheckToggleStroke.Thickness = 1

-- NOVO: Card de busca de jogador
local ESPSearchCard = Instance.new("Frame", ESPPage)
ESPSearchCard.Name = "ESPSearchCard"
ESPSearchCard.Size = UDim2.new(1, -40, 0, 200)
ESPSearchCard.Position = UDim2.new(0, 20, 0, 180)
ESPSearchCard.BackgroundColor3 = Theme.Secondary
local ESPSearchCorner = Instance.new("UICorner", ESPSearchCard)
ESPSearchCorner.CornerRadius = UDim.new(0, 8)
local ESPSearchStroke = Instance.new("UIStroke", ESPSearchCard)
ESPSearchStroke.Color = Theme.Stroke
ESPSearchStroke.Thickness = 1

local ESPSearchTitle = Instance.new("TextLabel", ESPSearchCard)
ESPSearchTitle.Text = "Focar em Jogador Específico"
ESPSearchTitle.Size = UDim2.new(1, -20, 0, 30)
ESPSearchTitle.Position = UDim2.new(0, 10, 0, 10)
ESPSearchTitle.BackgroundTransparency = 1
ESPSearchTitle.Font = Enum.Font.SourceSansSemibold
ESPSearchTitle.TextColor3 = Theme.Accent
ESPSearchTitle.TextSize = 18
ESPSearchTitle.TextXAlignment = Enum.TextXAlignment.Left

local ESPSearchDesc = Instance.new("TextLabel", ESPSearchCard)
ESPSearchDesc.Text = "Digite o nome e pressione ENTER. Use TAB para autocompletar."
ESPSearchDesc.Size = UDim2.new(1, -20, 0, 20)
ESPSearchDesc.Position = UDim2.new(0, 10, 0, 45)
ESPSearchDesc.BackgroundTransparency = 1
ESPSearchDesc.Font = Enum.Font.SourceSans
ESPSearchDesc.TextColor3 = Theme.TextSecondary
ESPSearchDesc.TextSize = 14
ESPSearchDesc.TextXAlignment = Enum.TextXAlignment.Left

local ESPSearchTextBox = Instance.new("TextBox", ESPSearchCard)
ESPSearchTextBox.Size = UDim2.new(1, -20, 0, 40)
ESPSearchTextBox.Position = UDim2.new(0, 10, 0, 75)
ESPSearchTextBox.BackgroundColor3 = Theme.Primary
ESPSearchTextBox.Font = Enum.Font.SourceSans
ESPSearchTextBox.TextColor3 = Theme.Text
ESPSearchTextBox.PlaceholderText = "Nome do jogador..."
ESPSearchTextBox.PlaceholderColor3 = Theme.TextSecondary
ESPSearchTextBox.Text = ""  -- CORRIGIDO: Começa vazio
ESPSearchTextBox.TextSize = 16
ESPSearchTextBox.ClearTextOnFocus = false
local ESPSearchTextBoxCorner = Instance.new("UICorner", ESPSearchTextBox)
ESPSearchTextBoxCorner.CornerRadius = UDim.new(0, 6)
local ESPSearchTextBoxStroke = Instance.new("UIStroke", ESPSearchTextBox)
ESPSearchTextBoxStroke.Color = Theme.Stroke

-- Container para mostrar jogador focado
local ESPFocusedContainer = Instance.new("Frame", ESPSearchCard)
ESPFocusedContainer.Size = UDim2.new(1, -20, 0, 50)
ESPFocusedContainer.Position = UDim2.new(0, 10, 0, 130)
ESPFocusedContainer.BackgroundColor3 = Theme.Success
ESPFocusedContainer.Visible = false
local ESPFocusedCorner = Instance.new("UICorner", ESPFocusedContainer)
ESPFocusedCorner.CornerRadius = UDim.new(0, 6)

local ESPFocusedLabel = Instance.new("TextLabel", ESPFocusedContainer)
ESPFocusedLabel.Text = "Focado: Ninguém"
ESPFocusedLabel.Size = UDim2.new(1, -80, 1, 0)
ESPFocusedLabel.Position = UDim2.new(0, 10, 0, 0)
ESPFocusedLabel.BackgroundTransparency = 1
ESPFocusedLabel.Font = Enum.Font.SourceSansBold
ESPFocusedLabel.TextColor3 = Theme.Text
ESPFocusedLabel.TextSize = 16
ESPFocusedLabel.TextXAlignment = Enum.TextXAlignment.Left

local ESPClearFocusBtn = Instance.new("TextButton", ESPFocusedContainer)
ESPClearFocusBtn.Text = "X"
ESPClearFocusBtn.Size = UDim2.new(0, 40, 0, 35)
ESPClearFocusBtn.Position = UDim2.new(1, -50, 0.5, -17.5)
ESPClearFocusBtn.BackgroundColor3 = Theme.Error
ESPClearFocusBtn.Font = Enum.Font.SourceSansBold
ESPClearFocusBtn.TextColor3 = Theme.Text
ESPClearFocusBtn.TextSize = 18
local ESPClearFocusBtnCorner = Instance.new("UICorner", ESPClearFocusBtn)
ESPClearFocusBtnCorner.CornerRadius = UDim.new(0, 6)


--[[============================================================
    FUNÇÕES AUXILIARES E ANIMAÇÕES
============================================================]]--
local function CreateButtonHover(button, hoverColor, defaultColor)
    button.MouseEnter:Connect(function() TweenService:Create(button, AnimationInfo.Fast, {BackgroundColor3 = hoverColor}):Play() end)
    button.MouseLeave:Connect(function() TweenService:Create(button, AnimationInfo.Fast, {BackgroundColor3 = defaultColor}):Play() end)
end

local function CreateSidebarButton(text, icon, positionY, associatedPage)
    local btn = Instance.new("TextButton", Sidebar)
    btn.Name = text .. "Btn"
    btn.RichText = true
    btn.Text = string.format("<font color='#%s'>%s</font>  %s", Theme.Accent:ToHex(), icon, text)
    btn.Size = UDim2.new(1, -20, 0, 40)
    btn.Position = UDim2.new(0, 10, 0, positionY)
    btn.BackgroundColor3 = Theme.Primary
    btn.Font = Enum.Font.SourceSans
    btn.TextColor3 = Theme.TextSecondary
    btn.TextSize = 16
    btn.TextXAlignment = Enum.TextXAlignment.Left
    local corner = Instance.new("UICorner", btn)
    corner.CornerRadius = UDim.new(0, 8)
    
    btn.MouseEnter:Connect(function()
        TweenService:Create(btn, AnimationInfo.Fast, {TextColor3 = Theme.Text}):Play()
        if ActivePage ~= associatedPage then TweenService:Create(btn, AnimationInfo.Fast, {BackgroundColor3 = Theme.Secondary}):Play() end
    end)
    btn.MouseLeave:Connect(function()
        TweenService:Create(btn, AnimationInfo.Fast, {TextColor3 = Theme.TextSecondary}):Play()
        if ActivePage ~= associatedPage then TweenService:Create(btn, AnimationInfo.Fast, {BackgroundColor3 = Theme.Primary}):Play() end
    end)
    return btn
end

local function ShowPage(pageToShow, associatedButton)
    if ActivePage == pageToShow then return end
    ActivePage = pageToShow
    
    for _, page in ipairs(AllPages) do
        page.Visible = (page == pageToShow)
    end
    
    TweenService:Create(SelectionIndicator, AnimationInfo.Medium, {Position = UDim2.new(0, 0, 0, associatedButton.Position.Y.Offset)}):Play()
    
    for _, child in ipairs(Sidebar:GetChildren()) do
        if child:IsA("TextButton") then
            local isSelected = (child == associatedButton)
            local targetColor = isSelected and Theme.Accent or Theme.Primary
            local targetTextColor = isSelected and Theme.Text or Theme.TextSecondary

            TweenService:Create(child, AnimationInfo.Fast, {
                BackgroundColor3 = targetColor,
                TextColor3 = targetTextColor
            }):Play()
        end
    end
end

local DashboardBtn = CreateSidebarButton("Dashboard", "🏠", 20, DashboardPage)
local ScriptsBtn = CreateSidebarButton("Scripts", "📜", 70, ScriptsPage)
local ESPBtn = CreateSidebarButton("ESP", "👁️", 120, ESPPage)
local AimbotBtn = CreateSidebarButton("Aimbot", "🎯", 170, AimbotPage)
local DiversosBtn = CreateSidebarButton("Diversos", "⚙️", 220, DiversosPage)
-- REMOVIDO: CopierBtn foi completamente removido

DashboardBtn.MouseButton1Click:Connect(function() ShowPage(DashboardPage, DashboardBtn) end)
ScriptsBtn.MouseButton1Click:Connect(function() ShowPage(ScriptsPage, ScriptsBtn) end)
ESPBtn.MouseButton1Click:Connect(function() ShowPage(ESPPage, ESPBtn) end)
AimbotBtn.MouseButton1Click:Connect(function() ShowPage(AimbotPage, AimbotBtn) end)
DiversosBtn.MouseButton1Click:Connect(function() ShowPage(DiversosPage, DiversosBtn) end)

--[[============================================================
    UI E LÓGICA DA PÁGINA DIVERSOS
============================================================]]--

local DiversosTitle = Instance.new("TextLabel", DiversosPage)
DiversosTitle.Text = "Diversos"
DiversosTitle.Size = UDim2.new(1, -40, 0, 40)
DiversosTitle.Position = UDim2.new(0, 20, 0, 20)
DiversosTitle.BackgroundTransparency = 1
DiversosTitle.Font = Enum.Font.SourceSansSemibold
DiversosTitle.TextColor3 = Theme.Accent
DiversosTitle.TextSize = 24
DiversosTitle.TextXAlignment = Enum.TextXAlignment.Left

local DiversosDesc = Instance.new("TextLabel", DiversosPage)
DiversosDesc.Text = "Funcionalidades diversas para melhorar sua experiência."
DiversosDesc.Size = UDim2.new(1, -40, 0, 30)
DiversosDesc.Position = UDim2.new(0, 20, 0, 60)
DiversosDesc.BackgroundTransparency = 1
DiversosDesc.Font = Enum.Font.SourceSans
DiversosDesc.TextColor3 = Theme.TextSecondary
DiversosDesc.TextSize = 16
DiversosDesc.TextXAlignment = Enum.TextXAlignment.Left

-- Toggle de Pulo Infinito
local InfiniteJumpToggle = Instance.new("TextButton", DiversosPage)
InfiniteJumpToggle.Text = "Pulo Infinito: DESATIVADO"
InfiniteJumpToggle.Size = UDim2.new(0, 200, 0, 50)
InfiniteJumpToggle.Position = UDim2.new(0, 20, 0, 110)
InfiniteJumpToggle.BackgroundColor3 = Theme.Error
InfiniteJumpToggle.Font = Enum.Font.SourceSansBold
InfiniteJumpToggle.TextColor3 = Theme.Text
InfiniteJumpToggle.TextSize = 16
local InfiniteJumpCorner = Instance.new("UICorner", InfiniteJumpToggle)
InfiniteJumpCorner.CornerRadius = UDim.new(0, 8)
local InfiniteJumpStroke = Instance.new("UIStroke", InfiniteJumpToggle)
InfiniteJumpStroke.Color = Theme.Stroke
InfiniteJumpStroke.Thickness = 1

-- Toggle de Velocidade
local SpeedToggle = Instance.new("TextButton", DiversosPage)
SpeedToggle.Text = "Velocidade: DESATIVADO"
SpeedToggle.Size = UDim2.new(0, 200, 0, 50)
SpeedToggle.Position = UDim2.new(0, 240, 0, 110)
SpeedToggle.BackgroundColor3 = Theme.Error
SpeedToggle.Font = Enum.Font.SourceSansBold
SpeedToggle.TextColor3 = Theme.Text
SpeedToggle.TextSize = 16
local SpeedToggleCorner = Instance.new("UICorner", SpeedToggle)
SpeedToggleCorner.CornerRadius = UDim.new(0, 8)
local SpeedToggleStroke = Instance.new("UIStroke", SpeedToggle)
SpeedToggleStroke.Color = Theme.Stroke
SpeedToggleStroke.Thickness = 1

-- Slider de Velocidade
local SpeedContainer = Instance.new("Frame", DiversosPage)
SpeedContainer.Size = UDim2.new(1, -40, 0, 80)
SpeedContainer.Position = UDim2.new(0, 20, 0, 180)
SpeedContainer.BackgroundColor3 = Theme.Secondary
local SpeedContainerCorner = Instance.new("UICorner", SpeedContainer)
SpeedContainerCorner.CornerRadius = UDim.new(0, 8)
local SpeedContainerStroke = Instance.new("UIStroke", SpeedContainer)
SpeedContainerStroke.Color = Theme.Stroke

local SpeedLabel = Instance.new("TextLabel", SpeedContainer)
SpeedLabel.Text = "Velocidade: 16 (Padrão)"
SpeedLabel.Size = UDim2.new(1, -20, 0, 25)
SpeedLabel.Position = UDim2.new(0, 10, 0, 10)
SpeedLabel.BackgroundTransparency = 1
SpeedLabel.Font = Enum.Font.SourceSansSemibold
SpeedLabel.TextColor3 = Theme.Text
SpeedLabel.TextSize = 16
SpeedLabel.TextXAlignment = Enum.TextXAlignment.Left

local SpeedTrack = Instance.new("Frame", SpeedContainer)
SpeedTrack.Size = UDim2.new(1, -20, 0, 8)
SpeedTrack.Position = UDim2.new(0, 10, 0, 45)
SpeedTrack.BackgroundColor3 = Theme.Primary
local SpeedTrackCorner = Instance.new("UICorner", SpeedTrack)
SpeedTrackCorner.CornerRadius = UDim.new(1, 0)

local SpeedFill = Instance.new("Frame", SpeedTrack)
SpeedFill.BackgroundColor3 = Theme.Accent
SpeedFill.Size = UDim2.new(0, 0, 1, 0)
local SpeedFillCorner = Instance.new("UICorner", SpeedFill)
SpeedFillCorner.CornerRadius = UDim.new(1, 0)

local SpeedHandle = Instance.new("TextButton", SpeedTrack)
SpeedHandle.Size = UDim2.new(0, 16, 0, 16)
SpeedHandle.AnchorPoint = Vector2.new(0.5, 0.5)
SpeedHandle.Position = UDim2.new(0, 0, 0.5, 0)
SpeedHandle.BackgroundColor3 = Theme.Text
SpeedHandle.Text = ""
local SpeedHandleCorner = Instance.new("UICorner", SpeedHandle)
SpeedHandleCorner.CornerRadius = UDim.new(1, 0)

-- Variáveis
local infiniteJumpEnabled = false
local speedEnabled = false
local walkSpeed = 16
local infiniteJumpConnection = nil

--[[============================================================
    LÓGICA DA PÁGINA DIVERSOS
============================================================]]--

-- Lógica do Pulo Infinito
InfiniteJumpToggle.MouseButton1Click:Connect(function()
    infiniteJumpEnabled = not infiniteJumpEnabled
    InfiniteJumpToggle.Text = "Pulo Infinito: " .. (infiniteJumpEnabled and "ATIVADO" or "DESATIVADO")
    InfiniteJumpToggle.BackgroundColor3 = infiniteJumpEnabled and Theme.Success or Theme.Error
    
    if infiniteJumpEnabled then
        infiniteJumpConnection = UserInputService.JumpRequest:Connect(function()
            if Player.Character then
                local humanoid = Player.Character:FindFirstChildOfClass("Humanoid")
                if humanoid then
                    humanoid:ChangeState(Enum.HumanoidStateType.Jumping)
                end
            end
        end)
    else
        if infiniteJumpConnection then
            infiniteJumpConnection:Disconnect()
            infiniteJumpConnection = nil
        end
    end
end)

-- Hover para Pulo Infinito
InfiniteJumpToggle.MouseEnter:Connect(function()
    if not infiniteJumpEnabled then
        TweenService:Create(InfiniteJumpToggle, AnimationInfo.Fast, {BackgroundColor3 = Theme.AccentHover}):Play()
    end
end)
InfiniteJumpToggle.MouseLeave:Connect(function()
    local targetColor = infiniteJumpEnabled and Theme.Success or Theme.Error
    TweenService:Create(InfiniteJumpToggle, AnimationInfo.Fast, {BackgroundColor3 = targetColor}):Play()
end)

-- Lógica do Toggle de Velocidade
SpeedToggle.MouseButton1Click:Connect(function()
    speedEnabled = not speedEnabled
    SpeedToggle.Text = "Velocidade: " .. (speedEnabled and "ATIVADO" or "DESATIVADO")
    SpeedToggle.BackgroundColor3 = speedEnabled and Theme.Success or Theme.Error
    
    if speedEnabled then
        -- Aplica velocidade ao personagem atual
        if Player.Character then
            local humanoid = Player.Character:FindFirstChildOfClass("Humanoid")
            if humanoid then
                humanoid.WalkSpeed = walkSpeed
            end
        end
        
        -- Mantém a velocidade ao respawnar
        Player.CharacterAdded:Connect(function(character)
            if speedEnabled then
                local humanoid = character:WaitForChild("Humanoid")
                humanoid.WalkSpeed = walkSpeed
            end
        end)
    else
        -- Reseta para velocidade padrão
        if Player.Character then
            local humanoid = Player.Character:FindFirstChildOfClass("Humanoid")
            if humanoid then
                humanoid.WalkSpeed = 16
            end
        end
    end
end)

-- Hover para Velocidade
SpeedToggle.MouseEnter:Connect(function()
    if not speedEnabled then
        TweenService:Create(SpeedToggle, AnimationInfo.Fast, {BackgroundColor3 = Theme.AccentHover}):Play()
    end
end)
SpeedToggle.MouseLeave:Connect(function()
    local targetColor = speedEnabled and Theme.Success or Theme.Error
    TweenService:Create(SpeedToggle, AnimationInfo.Fast, {BackgroundColor3 = targetColor}):Play()
end)

-- Lógica do Slider de Velocidade
local function updateSpeedSlider(value)
    walkSpeed = math.floor(value)
    local percentage = (walkSpeed - 16) / (100 - 16)
    SpeedLabel.Text = string.format("Velocidade: %d", walkSpeed)
    SpeedFill.Size = UDim2.new(percentage, 0, 1, 0)
    SpeedHandle.Position = UDim2.new(percentage, 0, 0.5, 0)
    
    -- Aplica imediatamente se estiver ativado
    if speedEnabled and Player.Character then
        local humanoid = Player.Character:FindFirstChildOfClass("Humanoid")
        if humanoid then
            humanoid.WalkSpeed = walkSpeed
        end
    end
end

SpeedHandle.MouseButton1Down:Connect(function()
    local moveConn, upConn
    moveConn = UserInputService.InputChanged:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseMovement then
            local percentage = math.clamp((input.Position.X - SpeedTrack.AbsolutePosition.X) / SpeedTrack.AbsoluteSize.X, 0, 1)
            local newValue = 16 + (100 - 16) * percentage
            updateSpeedSlider(newValue)
        end
    end)
    upConn = UserInputService.InputEnded:Connect(function(input)
        if input.UserInputType == Enum.UserInputType.MouseButton1 then
            moveConn:Disconnect()
            upConn:Disconnect()
        end
    end)
end)

-- Inicializa o slider
updateSpeedSlider(16)

-- Botões Rewind e Ball Mode
local RewindToggle = Instance.new("TextButton", DiversosPage)
RewindToggle.Text = "Rewind (Hold C): DESATIVADO"
RewindToggle.Size = UDim2.new(0, 220, 0, 50)
RewindToggle.Position = UDim2.new(0, 20, 0, 280)
RewindToggle.BackgroundColor3 = Theme.Error
RewindToggle.Font = Enum.Font.SourceSansBold
RewindToggle.TextColor3 = Theme.Text
RewindToggle.TextSize = 16
local RewindCorner = Instance.new("UICorner", RewindToggle)
RewindCorner.CornerRadius = UDim.new(0, 8)
local RewindStroke = Instance.new("UIStroke", RewindToggle)
RewindStroke.Color = Theme.Stroke

local BallModeToggle = Instance.new("TextButton", DiversosPage)
BallModeToggle.Text = "Ball Mode: DESATIVADO"
BallModeToggle.Size = UDim2.new(0, 220, 0, 50)
BallModeToggle.Position = UDim2.new(0, 250, 0, 280)
BallModeToggle.BackgroundColor3 = Theme.Error
BallModeToggle.Font = Enum.Font.SourceSansBold
BallModeToggle.TextColor3 = Theme.Text
BallModeToggle.TextSize = 16
local BallCorner = Instance.new("UICorner", BallModeToggle)
BallCorner.CornerRadius = UDim.new(0, 8)
local BallStroke = Instance.new("UIStroke", BallModeToggle)
BallStroke.Color = Theme.Stroke


--[[============================================================
    LÓGICA DOS SCRIPTS
============================================================]]--
for i, scriptData in ipairs(Scripts) do
    local scriptName, scriptUrl = scriptData[1], scriptData[2]
    
    local ScriptFrame = Instance.new("Frame", ScriptsPage)
    ScriptFrame.Size = UDim2.new(1, -40, 0, 60)
    ScriptFrame.BackgroundColor3 = Theme.Secondary
    ScriptFrame.LayoutOrder = i
    local ScriptCorner = Instance.new("UICorner", ScriptFrame)
    ScriptCorner.CornerRadius = UDim.new(0, 8)
    local ScriptStroke = Instance.new("UIStroke", ScriptFrame)
    ScriptStroke.Color = Theme.Stroke
    
    local ScriptNameLabel = Instance.new("TextLabel", ScriptFrame)
    ScriptNameLabel.Text = scriptName
    ScriptNameLabel.Size = UDim2.new(0.7, -15, 1, 0)
    ScriptNameLabel.Position = UDim2.new(0, 15, 0, 0)
    ScriptNameLabel.BackgroundTransparency = 1
    ScriptNameLabel.Font = Enum.Font.SourceSansSemibold
    ScriptNameLabel.TextColor3 = Theme.Text
    ScriptNameLabel.TextSize = 16
    ScriptNameLabel.TextXAlignment = Enum.TextXAlignment.Left
    
    local ExecuteBtn = Instance.new("TextButton", ScriptFrame)
    ExecuteBtn.Text = "EXECUTAR"
    ExecuteBtn.Size = UDim2.new(0, 100, 0, 35)
    ExecuteBtn.Position = UDim2.new(1, -110, 0.5, -17.5)
    ExecuteBtn.BackgroundColor3 = Theme.Accent
    ExecuteBtn.Font = Enum.Font.SourceSansBold
    ExecuteBtn.TextColor3 = Theme.Text
    ExecuteBtn.TextSize = 14
    local ExecCorner = Instance.new("UICorner", ExecuteBtn)
    ExecCorner.CornerRadius = UDim.new(0, 5)
    
    CreateButtonHover(ExecuteBtn, Theme.AccentHover, Theme.Accent)
    
    ExecuteBtn.MouseButton1Click:Connect(function()
        ExecuteBtn.Text = "..."
        TweenService:Create(ExecuteBtn, AnimationInfo.Fast, {BackgroundColor3 = Theme.Warning}):Play()
        spawn(function()
            local success, err = pcall(function() loadstring(game:HttpGet(scriptUrl))() end)
            task.wait(0.5)
            if success then
                ExecuteBtn.Text = "OK!"
                TweenService:Create(ExecuteBtn, AnimationInfo.Fast, {BackgroundColor3 = Theme.Success}):Play()
            else
                ExecuteBtn.Text = "ERRO"
                TweenService:Create(ExecuteBtn, AnimationInfo.Fast, {BackgroundColor3 = Theme.Error}):Play()
                warn("Erro ao executar '" .. scriptName .. "': " .. tostring(err))
            end
            task.wait(2)
            ExecuteBtn.Text = "EXECUTAR"
            TweenService:Create(ExecuteBtn, AnimationInfo.Fast, {BackgroundColor3 = Theme.Accent}):Play()
        end)
    end)
end

--[[============================================================
    LÓGICA DO ESP
============================================================]]--
local ESPEnabled = false
local ESPObjects = {}
local espConnection = nil
local ESPShowDistance = false  -- NOVO: Controla se mostra distância
local ESPTargetPlayer = nil  -- NOVO: Jogador específico para focar (se houver)
local HighlightEnabled = false  -- NOVO: Controla o contorno dos personagens
local HighlightObjects = {}
local TeamCheckEnabled = false  -- NOVO: Controla se verifica times (verde para aliados, vermelho para inimigos)
-- Variáveis Rewind e Ball Mode
local rewindEnabled = false
local rewindPositions = {}
local rewindConnection = nil
local maxRewindPositions = 150
local rewindActive = false
local rewindInputConnection = nil
local rewindUpdateConnection = nil

local ballModeEnabled = false
local ballSpeed = 35
local ballJumpPower = 60
local ballConnection = nil
local ballJumpConnection = nil

  -- NOVO: Armazena os highlights criados

local function RemoveESP(player)
    if ESPObjects[player] then
        ESPObjects[player].Gui:Destroy()
        ESPObjects[player] = nil
    end
end

local function CreateESP(player)
    if player == Player or ESPObjects[player] then return end

    local billboard = Instance.new("BillboardGui")
    billboard.Name = player.Name
    billboard.AlwaysOnTop = true
    billboard.Size = UDim2.new(0, 200, 0, 30)  -- MODIFICADO: Aumentado para caber a distância
    billboard.StudsOffset = Vector3.new(0, 3.5, 0)
    billboard.Enabled = false
    billboard.Parent = ScreenGui

    local nameLabel = Instance.new("TextLabel", billboard)
    nameLabel.Text = player.Name
    nameLabel.Size = UDim2.new(1, 0, 1, 0)
    nameLabel.BackgroundTransparency = 1
    nameLabel.Font = Enum.Font.SourceSansBold
    -- MODIFICADO: Cor verde para amigos, branco para outros
    nameLabel.TextColor3 = friendsList[player.Name] and Color3.fromRGB(34, 197, 94) or Color3.fromRGB(255, 255, 255)
    nameLabel.TextSize = 18
    nameLabel.TextStrokeTransparency = 0
    nameLabel.TextStrokeColor3 = Color3.new(0, 0, 0)

    ESPObjects[player] = { Gui = billboard, Label = nameLabel }
end

local function UpdateESP()
    -- Pega a posição do jogador local
    local myCharacter = Player.Character
    local myHRP = myCharacter and myCharacter:FindFirstChild("HumanoidRootPart")
    
    for _, player in ipairs(Players:GetPlayers()) do
        if player ~= Player then
            -- NOVO: Se há um alvo específico, mostra apenas ele
            if ESPTargetPlayer and player.Name ~= ESPTargetPlayer then
                if ESPObjects[player] then
                    ESPObjects[player].Gui.Enabled = false
                end
                continue
            end
            
            if not ESPObjects[player] then
                CreateESP(player)
            end
            
            local espData = ESPObjects[player]
            if espData then
                local character = player.Character
                local humanoid = character and character:FindFirstChildOfClass("Humanoid")
                local head = character and character:FindFirstChild("Head")
                local hrp = character and character:FindFirstChild("HumanoidRootPart")

                if head and humanoid and humanoid.Health > 0 then
                    espData.Gui.Adornee = head
                    espData.Gui.Enabled = true
                    
                    -- MODIFICADO: Só mostra distância se ESPShowDistance estiver ativado
                    if ESPShowDistance and myHRP and hrp then
                        local distance = math.floor((myHRP.Position - hrp.Position).Magnitude)
                        local distanceText = string.format(" [%dm]", distance)
                        espData.Label.Text = player.Name .. distanceText
                    else
                        espData.Label.Text = player.Name
                    end
                    
                    -- Cor: Verde para amigos, Branco para outros
                    if friendsList[player.Name] then
                        espData.Label.TextColor3 = Color3.fromRGB(34, 197, 94)  -- Verde para amigos
                    else
                        espData.Label.TextColor3 = Color3.fromRGB(255, 255, 255)  -- Branco para outros
                    end
                else
                    espData.Gui.Enabled = false
                end
            end
        end
    end
end

ESPToggle.MouseButton1Click:Connect(function()
    ESPEnabled = not ESPEnabled
    ESPToggle.Text = "ESP: " .. (ESPEnabled and "ATIVADO" or "DESATIVADO")
    local color = ESPEnabled and Theme.Success or Theme.Error
    TweenService:Create(ESPToggle, AnimationInfo.Fast, {BackgroundColor3 = color}):Play()

    if ESPEnabled then
        for _, player in ipairs(Players:GetPlayers()) do
            CreateESP(player)
        end
        espConnection = RunService.RenderStepped:Connect(UpdateESP)
    else
        if espConnection then
            espConnection:Disconnect()
            espConnection = nil
        end
        for player, _ in pairs(ESPObjects) do
            RemoveESP(player)
        end
        ESPObjects = {}
    end
end)

-- NOVO: Lógica do toggle de distância
ESPDistanceToggle.MouseButton1Click:Connect(function()
    ESPShowDistance = not ESPShowDistance
    ESPDistanceToggle.Text = "Mostrar Distância: " .. (ESPShowDistance and "SIM" or "NÃO")
    ESPDistanceToggle.BackgroundColor3 = ESPShowDistance and Theme.Success or Theme.Error
end)

-- Adiciona hover customizado que respeita o estado
ESPDistanceToggle.MouseEnter:Connect(function()
    if not ESPShowDistance then
        TweenService:Create(ESPDistanceToggle, AnimationInfo.Fast, {BackgroundColor3 = Theme.AccentHover}):Play()
    end
end)

ESPDistanceToggle.MouseLeave:Connect(function()
    local targetColor = ESPShowDistance and Theme.Success or Theme.Error
    TweenService:Create(ESPDistanceToggle, AnimationInfo.Fast, {BackgroundColor3 = targetColor}):Play()
end)

-- PLACEHOLDER: Lógica do toggle de Highlight será definida após as funções

-- NOVO: Função de autocompletar nome
local function autocompleteESPSearch()
    local text = ESPSearchTextBox.Text:lower()
    if text == "" then return end
    
    for _, p in ipairs(Players:GetPlayers()) do
        if p ~= Player and p.Name:lower():sub(1, #text) == text then
            ESPSearchTextBox.Text = p.Name
            -- Seleciona o texto autocompletado
            task.wait()
            ESPSearchTextBox.CursorPosition = #p.Name + 1
            return
        end
    end
end

-- NOVO: Função para focar em jogador específico
local function focusESPOnPlayer()
    local playerName = ESPSearchTextBox.Text
    local targetPlayer = Players:FindFirstChild(playerName)
    
    if not targetPlayer or targetPlayer == Player then
        ESPSearchTextBox.Text = ""
        return
    end
    
    ESPTargetPlayer = playerName
    ESPFocusedLabel.Text = "Focado: " .. playerName
    ESPFocusedContainer.Visible = true
    ESPSearchTextBox.Text = ""
    
    -- Atualiza ESP para mostrar apenas o jogador focado
    if ESPEnabled then
        UpdateESP()
    end
end

-- NOVO: Função para limpar foco
local function clearESPFocus()
    ESPTargetPlayer = nil
    ESPFocusedContainer.Visible = false
    
    -- Atualiza ESP para mostrar todos os jogadores novamente
    if ESPEnabled then
        UpdateESP()
    end
end

-- NOVO: Eventos da busca de jogador
ESPClearFocusBtn.MouseButton1Click:Connect(clearESPFocus)

-- NOVO: Detecta TAB para autocompletar (evento específico do TextBox)
ESPSearchTextBox:GetPropertyChangedSignal("Text"):Connect(function()
    -- Atualiza em tempo real enquanto digita
end)

-- Conexão direta com o TextBox para capturar TAB
local espSearchConnection
ESPSearchTextBox.Focused:Connect(function()
    espSearchConnection = UserInputService.InputBegan:Connect(function(input, gameProcessed)
        if input.KeyCode == Enum.KeyCode.Tab then
            autocompleteESPSearch()
        end
    end)
end)

ESPSearchTextBox.FocusLost:Connect(function(enterPressed)
    if espSearchConnection then
        espSearchConnection:Disconnect()
        espSearchConnection = nil
    end
    
    if enterPressed then
        focusESPOnPlayer()
    end
end)

CreateButtonHover(ESPDistanceToggle, Theme.AccentHover, Theme.Error)
CreateButtonHover(ESPClearFocusBtn, Color3.fromRGB(220, 38, 38), Theme.Error)

Players.PlayerAdded:Connect(function(player)
    if ESPEnabled then CreateESP(player) end
end)
Players.PlayerRemoving:Connect(RemoveESP)

--[[============================================================
    LÓGICA DO HIGHLIGHT (CONTORNO) - FUNÇÕES
============================================================]]--

-- Tabela para armazenar highlights
local highlightConnection = nil

-- Função para criar/atualizar highlights
local function UpdateHighlights()
    if not HighlightEnabled then return end

    for _, player in ipairs(Players:GetPlayers()) do
        if player ~= Player then
            local character = player.Character
            if character then
                local existingHighlight = character:FindFirstChild("ESPHighlight")

                -- Determina a cor baseada no time
                local outlineColor = Color3.fromRGB(255, 70, 70)  -- Padrão: vermelho

                if TeamCheckEnabled then
                    -- Verifica se está no mesmo time
                    if player.Team and Player.Team and player.Team == Player.Team then
                        outlineColor = Color3.fromRGB(70, 255, 70)  -- Verde para aliados
                    else
                        outlineColor = Color3.fromRGB(255, 70, 70)  -- Vermelho para inimigos
                    end
                end

                -- Se não tem highlight, cria
                if not existingHighlight then
                    local humanoid = character:FindFirstChildOfClass("Humanoid")
                    if humanoid and humanoid.Health > 0 then
                        local highlight = Instance.new("Highlight")
                        highlight.Name = "ESPHighlight"
                        highlight.FillColor = Color3.fromRGB(255, 0, 0)
                        highlight.FillTransparency = 1
                        highlight.OutlineColor = outlineColor
                        highlight.OutlineTransparency = 0
                        highlight.DepthMode = Enum.HighlightDepthMode.AlwaysOnTop
                        highlight.Parent = character

                        print("✓ Highlight criado para: " .. player.Name)
                    end
                else
                    -- Atualiza a cor do highlight existente
                    existingHighlight.OutlineColor = outlineColor
                end
            end
        end
    end
end

-- Função para remover todos os highlights
local function RemoveAllHighlights()
    for _, player in ipairs(Players:GetPlayers()) do
        if player.Character then
            local highlight = player.Character:FindFirstChild("ESPHighlight")
            if highlight then
                highlight:Destroy()
            end
        end
    end
end

-- Detecta quando personagens são adicionados
local function onCharacterAdded(character)
    if HighlightEnabled then
        task.wait(0.5)
        UpdateHighlights()
    end
end

-- Conecta eventos para jogadores existentes
for _, player in ipairs(Players:GetPlayers()) do
    if player ~= Player then
        player.CharacterAdded:Connect(onCharacterAdded)
    end
end

-- Conecta eventos para novos jogadores
Players.PlayerAdded:Connect(function(player)
    if player ~= Player then
        player.CharacterAdded:Connect(onCharacterAdded)
    end
end)

--[[============================================================
    LÓGICA DO TOGGLE DE HIGHLIGHT
============================================================]]--

-- NOVO: Lógica do toggle de Highlight (Contorno)
HighlightToggle.MouseButton1Click:Connect(function()
    HighlightEnabled = not HighlightEnabled
    HighlightToggle.Text = "Contorno: " .. (HighlightEnabled and "ATIVADO" or "DESATIVADO")
    HighlightToggle.BackgroundColor3 = HighlightEnabled and Theme.Success or Theme.Error
    
    if HighlightEnabled then
        print("Ativando Highlights...")
        
        -- Cria highlights iniciais
        UpdateHighlights()
        
        -- Inicia loop de atualização
        highlightConnection = RunService.Heartbeat:Connect(function()
            UpdateHighlights()
        end)
    else
        print("Desativando Highlights...")
        
        -- Para o loop
        if highlightConnection then
            highlightConnection:Disconnect()
            highlightConnection = nil
        end
        
        -- Remove todos os highlights
        RemoveAllHighlights()
    end
end)

-- Adiciona hover customizado para o botão de Highlight
HighlightToggle.MouseEnter:Connect(function()
    if not HighlightEnabled then
        TweenService:Create(HighlightToggle, AnimationInfo.Fast, {BackgroundColor3 = Theme.AccentHover}):Play()
    end
end)

HighlightToggle.MouseLeave:Connect(function()
    local targetColor = HighlightEnabled and Theme.Success or Theme.Error
    TweenService:Create(HighlightToggle, AnimationInfo.Fast, {BackgroundColor3 = targetColor}):Play()
end)

--[[============================================================
    LÓGICA DO TOGGLE DE VERIFICAR TIMES
============================================================]]--

-- NOVO: Lógica do toggle de Verificar Times
TeamCheckToggle.MouseButton1Click:Connect(function()
    TeamCheckEnabled = not TeamCheckEnabled
    TeamCheckToggle.Text = "Verificar Times: " .. (TeamCheckEnabled and "SIM" or "NÃO")
    TeamCheckToggle.BackgroundColor3 = TeamCheckEnabled and Theme.Success or Theme.Error

    -- Atualiza as cores dos highlights já existentes
    if HighlightEnabled then
        UpdateHighlights()
    end

    print("Verificação de Times: " .. (TeamCheckEnabled and "ATIVADA" or "DESATIVADA"))
end)

-- Adiciona hover customizado para o botão de Verificar Times
TeamCheckToggle.MouseEnter:Connect(function()
    if not TeamCheckEnabled then
        TweenService:Create(TeamCheckToggle, AnimationInfo.Fast, {BackgroundColor3 = Theme.AccentHover}):Play()
    end
end)

TeamCheckToggle.MouseLeave:Connect(function()
    local targetColor = TeamCheckEnabled and Theme.Success or Theme.Error
    TweenService:Create(TeamCheckToggle, AnimationInfo.Fast, {BackgroundColor3 = targetColor}):Play()
end)

--[[============================================================
    LÓGICA E UI COMPLETA DO AIMBOT (CORRIGIDO)
============================================================]]--
local fovCircle = Instance.new("Frame", ScreenGui)
fovCircle.BackgroundTransparency = 1  -- CORRIGIDO: Totalmente transparente (sem preenchimento)
fovCircle.BorderSizePixel = 0
fovCircle.Visible = false
fovCircle.AnchorPoint = Vector2.new(0.5, 0.5)
local fovCorner = Instance.new("UICorner", fovCircle)
fovCorner.CornerRadius = UDim.new(1, 0)
local fovStroke = Instance.new("UIStroke", fovCircle)
fovStroke.Color = Color3.fromRGB(255, 255, 255)  -- CORRIGIDO: Branco
fovStroke.Thickness = 2
fovStroke.Transparency = 0  -- CORRIGIDO: Borda totalmente visível

local function isVisible(part)
    if not aimbotWallCheck then return true end
    local origin = Camera.CFrame.Position
    local direction = (part.Position - origin)
    local ray = Ray.new(origin, direction.Unit * math.min(direction.Magnitude, 1000))
    local hitPart, _ = Workspace:FindPartOnRayWithIgnoreList(ray, {Player.Character}, false, true)
    if hitPart then
        return hitPart:IsDescendantOf(part.Parent)
    end
    return false
end

-- NOVO: Função para obter a melhor parte disponível do alvo (universal)
local function getBestTargetPart(character)
    -- Lista de partes em ordem de prioridade
    local partPriority = {
        aimbotTargetPart,  -- Parte escolhida pelo usuário
        "Head",
        "UpperTorso",
        "HumanoidRootPart",
        "Torso",
        "LowerTorso"
    }

    for _, partName in ipairs(partPriority) do
        local part = character:FindFirstChild(partName)
        if part and part:IsA("BasePart") then
            return part
        end
    end

    -- Fallback: retorna qualquer BasePart do personagem
    for _, part in ipairs(character:GetDescendants()) do
        if part:IsA("BasePart") and part.Name ~= "HumanoidRootPart" then
            return part
        end
    end

    return nil
end

-- NOVO: Calcula posição prevista do alvo baseado na velocidade
local function getPredictedPosition(targetPart)
    if not targetPart or not targetPart:IsA("BasePart") then
        return targetPart and targetPart.Position or Vector3.new()
    end

    local velocity = targetPart.AssemblyLinearVelocity or targetPart.Velocity or Vector3.new()
    local distance = (targetPart.Position - Camera.CFrame.Position).Magnitude
    local timeToHit = distance / 500  -- Ajuste baseado na velocidade do projétil (500 studs/s é padrão)

    -- Aplica prediction personalizada
    return targetPart.Position + (velocity * (timeToHit + aimbotPrediction))
end

-- MELHORADO: Função universalmente compatível com detecção automática de partes
local function getClosestPartToPoint(aimPoint)
    local closestPart = nil
    local shortestDist = aimbotFovRadius

    for _, p in ipairs(Players:GetPlayers()) do
        if p ~= Player and p.Character then
            -- Ignora amigos
            if friendsList[p.Name] then continue end

            -- Verifica team check
            if aimbotTeamCheck and p.Team == Player.Team then continue end

            -- Verifica se está vivo
            local humanoid = p.Character:FindFirstChildOfClass("Humanoid")
            if not (humanoid and humanoid.Health > 0) then continue end

            -- NOVO: Usa sistema de detecção automática de partes
            local targetBodyPart = getBestTargetPart(p.Character)
            if not targetBodyPart then continue end

            -- Calcula posição com prediction
            local predictedPos = getPredictedPosition(targetBodyPart)
            local pos, onScreen = Camera:WorldToViewportPoint(predictedPos)

            if onScreen then
                local dist = (Vector2.new(pos.X, pos.Y) - aimPoint).Magnitude
                if dist < shortestDist and isVisible(targetBodyPart) then
                    shortestDist = dist
                    closestPart = targetBodyPart
                end
            end
        end
    end
    return closestPart
end

-- MELHORADO: Suavização aprimorada com prediction
local function smoothLookAt(target)
    if not target or not target:IsA("BasePart") then return end

    local predictedPos = getPredictedPosition(target)
    local startCFrame = Camera.CFrame
    local endCFrame = CFrame.new(Camera.CFrame.Position, predictedPos)

    -- Suavização mais precisa
    local smoothness = 1 - aimbotSmoothingFactor
    local newCFrame = startCFrame:Lerp(endCFrame, smoothness)
    Camera.CFrame = newCFrame
end

-- MELHORADO: Modo mouse universal (funciona mesmo sem mousemoverel)
local function moveMouseTowards(target)
    if not target or not target:IsA("BasePart") then return end

    local predictedPos = getPredictedPosition(target)
    local targetScreenPos, onScreen = Camera:WorldToViewportPoint(predictedPos)
    if not onScreen then return end

    -- Tenta usar mousemoverel se disponível
    if mousemoverel then
        local mousePos = UserInputService:GetMouseLocation()
        local delta = Vector2.new(targetScreenPos.X - mousePos.X, targetScreenPos.Y - mousePos.Y)

        if delta.Magnitude < 1 then return end

        local moveVector = delta / mouseAimbotStrength
        mousemoverel(moveVector.X, moveVector.Y)
    else
        -- FALLBACK: Usa modo câmera se mousemoverel não estiver disponível
        smoothLookAt(target)
    end
end

local function isAimKeyPressed()
    if aimbotActivationKey == "Mouse2" then
        return UserInputService:IsMouseButtonPressed(Enum.UserInputType.MouseButton2)
    elseif aimbotActivationKey == "LeftControl" then
        return UserInputService:IsKeyDown(Enum.KeyCode.LeftControl)
    end
    return false
end

--[[============================================================
    SISTEMA DE SILENT AIM - UNIVERSAL E SIMPLES
============================================================]]--

-- MELHORADO: Função para obter o alvo mais próximo dentro do FOV (universal)
local function getSilentAimTarget()
    local mousePos = UserInputService:GetMouseLocation()
    local closestPart = nil
    local shortestDist = aimbotFovRadius

    for _, player in ipairs(Players:GetPlayers()) do
        if player ~= Player and player.Character then
            if friendsList[player.Name] then continue end
            if aimbotTeamCheck and player.Team == Player.Team then continue end

            local humanoid = player.Character:FindFirstChildOfClass("Humanoid")
            if not (humanoid and humanoid.Health > 0) then continue end

            -- NOVO: Usa detecção automática de partes
            local targetBodyPart = getBestTargetPart(player.Character)
            if not targetBodyPart then continue end

            -- NOVO: Usa posição prevista
            local predictedPos = getPredictedPosition(targetBodyPart)
            local pos, onScreen = Camera:WorldToViewportPoint(predictedPos)
            if not onScreen then continue end

            local dist = (Vector2.new(pos.X, pos.Y) - mousePos).Magnitude

            if dist < shortestDist then
                if aimbotWallCheck and not isVisible(targetBodyPart) then continue end
                shortestDist = dist
                closestPart = targetBodyPart
            end
        end
    end

    return closestPart
end

-- Variáveis do Silent Aim
local currentSilentTarget = nil
local silentAimActive = false

-- MELHORADO: Hook Universal do Mouse com prediction
local function setupMouseHitHook()
    pcall(function()
        local mt = getrawmetatable(game)
        local oldIndex = mt.__index
        setreadonly(mt, false)

        mt.__index = newcclosure(function(self, key)
            if silentAimEnabled and silentAimActive and currentSilentTarget then
                if tostring(self):find("Mouse") and (key == "Hit" or key == "Target") then
                    if math.random(1, 100) <= silentAimHitChance then
                        if key == "Hit" then
                            -- NOVO: Usa posição prevista no Silent Aim
                            local predictedPos = getPredictedPosition(currentSilentTarget)
                            return CFrame.new(predictedPos)
                        elseif key == "Target" then
                            return currentSilentTarget
                        end
                    end
                end
            end
            return oldIndex(self, key)
        end)

        setreadonly(mt, true)
        print("✓ Silent Aim ativado com prediction melhorada")
    end)
end

-- Detecta tiro
UserInputService.InputBegan:Connect(function(input, gameProcessed)
    if gameProcessed or input.UserInputType ~= Enum.UserInputType.MouseButton1 then return end
    if silentAimEnabled then
        currentSilentTarget = getSilentAimTarget()
        silentAimActive = true
    end
end)

UserInputService.InputEnded:Connect(function(input)
    if input.UserInputType == Enum.UserInputType.MouseButton1 then
        task.wait(0.05)
        silentAimActive = false
        currentSilentTarget = nil
    end
end)

-- Atualiza alvo para armas automáticas
task.spawn(function()
    while task.wait(0.1) do
        if silentAimEnabled and silentAimActive then
            local newTarget = getSilentAimTarget()
            if newTarget then currentSilentTarget = newTarget end
        end
    end
end)

-- Inicializa
setupMouseHitHook()


-- UI do Aimbot
local AimbotTitle = Instance.new("TextLabel", AimbotPage)
AimbotTitle.Text = "Sistema Aimbot"
AimbotTitle.Size = UDim2.new(1, -40, 0, 40)
AimbotTitle.BackgroundTransparency = 1
AimbotTitle.Font = Enum.Font.SourceSansSemibold
AimbotTitle.TextColor3 = Theme.Accent
AimbotTitle.TextSize = 24
AimbotTitle.TextXAlignment = Enum.TextXAlignment.Left
AimbotTitle.LayoutOrder = 1

local AimbotDesc = Instance.new("TextLabel", AimbotPage)
AimbotDesc.Text = "Mira automaticamente em inimigos próximos. Pressione a tecla de ativação para travar a mira."
AimbotDesc.Size = UDim2.new(1, -40, 0, 30)
AimbotDesc.BackgroundTransparency = 1
AimbotDesc.Font = Enum.Font.SourceSans
AimbotDesc.TextColor3 = Theme.TextSecondary
AimbotDesc.TextSize = 16
AimbotDesc.TextXAlignment = Enum.TextXAlignment.Left
AimbotDesc.LayoutOrder = 2

-- NOVO: Card de Jogadores Próximos
local NearbyPlayersCard = Instance.new("Frame", AimbotPage)
NearbyPlayersCard.Name = "NearbyPlayersCard"
NearbyPlayersCard.Size = UDim2.new(1, -40, 0, 250)
NearbyPlayersCard.BackgroundColor3 = Theme.Secondary
NearbyPlayersCard.LayoutOrder = 3
local NearbyCardCorner = Instance.new("UICorner", NearbyPlayersCard)
NearbyCardCorner.CornerRadius = UDim.new(0, 8)
local NearbyCardStroke = Instance.new("UIStroke", NearbyPlayersCard)
NearbyCardStroke.Color = Theme.Stroke
NearbyCardStroke.Thickness = 1

local NearbyTitle = Instance.new("TextLabel", NearbyPlayersCard)
NearbyTitle.Text = "Jogadores Próximos"
NearbyTitle.Size = UDim2.new(1, -20, 0, 30)
NearbyTitle.Position = UDim2.new(0, 10, 0, 5)
NearbyTitle.BackgroundTransparency = 1
NearbyTitle.Font = Enum.Font.SourceSansSemibold
NearbyTitle.TextColor3 = Theme.Accent
NearbyTitle.TextSize = 18
NearbyTitle.TextXAlignment = Enum.TextXAlignment.Left

local NearbyScrollFrame = Instance.new("ScrollingFrame", NearbyPlayersCard)
NearbyScrollFrame.Name = "NearbyScroll"
NearbyScrollFrame.Size = UDim2.new(1, -20, 1, -45)
NearbyScrollFrame.Position = UDim2.new(0, 10, 0, 35)
NearbyScrollFrame.BackgroundTransparency = 1
NearbyScrollFrame.ScrollBarThickness = 4
NearbyScrollFrame.ScrollBarImageColor3 = Theme.Accent
NearbyScrollFrame.BorderSizePixel = 0

local NearbyLayout = Instance.new("UIListLayout", NearbyScrollFrame)
NearbyLayout.Padding = UDim.new(0, 5)
NearbyLayout.SortOrder = Enum.SortOrder.Name

NearbyLayout:GetPropertyChangedSignal("AbsoluteContentSize"):Connect(function()
    NearbyScrollFrame.CanvasSize = UDim2.new(0, 0, 0, NearbyLayout.AbsoluteContentSize.Y)
end)

local function createAimbotToggle(text, order, callback)
    local Toggle = Instance.new("TextButton", AimbotPage)
    Toggle.Size = UDim2.new(1, -40, 0, 50)
    Toggle.BackgroundColor3 = Theme.Error
    Toggle.Font = Enum.Font.SourceSansBold
    Toggle.TextColor3 = Theme.Text
    Toggle.TextSize = 16
    Toggle.LayoutOrder = order
    local ToggleCorner = Instance.new("UICorner", Toggle)
    ToggleCorner.CornerRadius = UDim.new(0, 8)
    
    local function updateState(enabled)
        Toggle.Text = text .. ": " .. (enabled and "ATIVADO" or "DESATIVADO")
        local color = enabled and Theme.Success or Theme.Error
        TweenService:Create(Toggle, AnimationInfo.Fast, {BackgroundColor3 = color}):Play()
    end
    
    Toggle.MouseButton1Click:Connect(function()
        callback(updateState)
    end)
    
    return updateState
end

local function createAimbotSlider(name, min, max, initialValue, order, callback)
    local Container = Instance.new("Frame", AimbotPage)
    Container.Name = name:gsub(" ", "") .. "Slider"
    Container.Size = UDim2.new(1, -40, 0, 60)
    Container.BackgroundTransparency = 1
    Container.LayoutOrder = order
    
    local Label = Instance.new("TextLabel", Container)
    Label.Size = UDim2.new(1, 0, 0, 25)
    Label.BackgroundTransparency = 1
    Label.Font = Enum.Font.SourceSans
    Label.TextColor3 = Theme.Text
    Label.TextSize = 16
    Label.TextXAlignment = Enum.TextXAlignment.Left
    
    local Track = Instance.new("Frame", Container)
    Track.Size = UDim2.new(1, 0, 0, 8)
    Track.Position = UDim2.new(0, 0, 0, 30)
    Track.BackgroundColor3 = Theme.Secondary
    local TrackCorner = Instance.new("UICorner", Track)
    TrackCorner.CornerRadius = UDim.new(1, 0)
    
    local Fill = Instance.new("Frame", Track)
    Fill.BackgroundColor3 = Theme.Accent
    local FillCorner = Instance.new("UICorner", Fill)
    FillCorner.CornerRadius = UDim.new(1, 0)
    
    local Handle = Instance.new("TextButton", Track)
    Handle.Size = UDim2.new(0, 16, 0, 16)
    Handle.AnchorPoint = Vector2.new(0.5, 0.5)
    Handle.Position = UDim2.new(0, 0, 0.5, 0)
    Handle.BackgroundColor3 = Theme.Text
    Handle.Text = ""
    local HandleCorner = Instance.new("UICorner", Handle)
    HandleCorner.CornerRadius = UDim.new(1, 0)
    
    local function updateSlider(value)
        local percentage = (value - min) / (max - min)
        Label.Text = string.format("%s: %.2f", name, value)
        Fill.Size = UDim2.new(percentage, 0, 1, 0)
        Handle.Position = UDim2.new(percentage, 0, 0.5, 0)
        callback(value)
    end
    
    Handle.MouseButton1Down:Connect(function()
        local moveConn, upConn
        moveConn = UserInputService.InputChanged:Connect(function(input)
            if input.UserInputType == Enum.UserInputType.MouseMovement then
                local percentage = math.clamp((input.Position.X - Track.AbsolutePosition.X) / Track.AbsoluteSize.X, 0, 1)
                local newValue = min + (max - min) * percentage
                updateSlider(newValue)
            end
        end)
        upConn = UserInputService.InputEnded:Connect(function(input)
            if input.UserInputType == Enum.UserInputType.MouseButton1 then
                moveConn:Disconnect()
                upConn:Disconnect()
            end
        end)
    end)
    
    updateSlider(initialValue)
    return Container
end

-- CORRIGIDO: Função de seleção agora atualiza a variável global corretamente
local function createAimbotSelector(name, options, order, callback)
    local Container = Instance.new("Frame", AimbotPage)
    Container.Size = UDim2.new(1, -40, 0, 50)
    Container.BackgroundColor3 = Theme.Secondary
    Container.LayoutOrder = order
    local ContainerCorner = Instance.new("UICorner", Container)
    ContainerCorner.CornerRadius = UDim.new(0, 8)
    
    local Label = Instance.new("TextLabel", Container)
    Label.Size = UDim2.new(1, -120, 1, 0)
    Label.Position = UDim2.new(0, 15, 0, 0)
    Label.BackgroundTransparency = 1
    Label.Font = Enum.Font.SourceSans
    Label.TextColor3 = Theme.Text
    Label.TextSize = 16
    Label.TextXAlignment = Enum.TextXAlignment.Left

    local Button = Instance.new("TextButton", Container)
    Button.Size = UDim2.new(0, 100, 0, 35)
    Button.Position = UDim2.new(1, -110, 0.5, -17.5)
    Button.BackgroundColor3 = Theme.Accent
    Button.Font = Enum.Font.SourceSansBold
    Button.TextColor3 = Theme.Text
    Button.TextSize = 14
    Button.Text = "MUDAR"
    local BtnCorner = Instance.new("UICorner", Button)
    BtnCorner.CornerRadius = UDim.new(0, 5)
    CreateButtonHover(Button, Theme.AccentHover, Theme.Accent)
    
    local currentIndex = 1
    local function updateSelector()
        Label.Text = string.format("%s: %s", name, options[currentIndex])
        callback(options[currentIndex])
    end
    
    Button.MouseButton1Click:Connect(function()
        currentIndex = (currentIndex % #options) + 1
        updateSelector()
    end)
    
    updateSelector()
end

local updateAimbotToggle = createAimbotToggle("Aimbot", 4, function(update)
    aimbotEnabled = not aimbotEnabled
    update(aimbotEnabled)
end)
updateAimbotToggle(aimbotEnabled)

local updateTeamCheck = createAimbotToggle("Verificar Time", 5, function(update)
    aimbotTeamCheck = not aimbotTeamCheck
    update(aimbotTeamCheck)
end)
updateTeamCheck(aimbotTeamCheck)

local updateWallCheck = createAimbotToggle("Verificar Parede", 6, function(update)
    aimbotWallCheck = not aimbotWallCheck
    update(aimbotWallCheck)
end)
updateWallCheck(aimbotWallCheck)

local updateShowFov = createAimbotToggle("Exibir FOV", 7, function(update)
    aimbotShowFov = not aimbotShowFov
    update(aimbotShowFov)
end)
updateShowFov(aimbotShowFov)

createAimbotSlider("Raio do FOV", 20, 500, aimbotFovRadius, 8, function(value)
    aimbotFovRadius = value
end)

local cameraSmoothSlider = createAimbotSlider("Suavização", 0, 0.95, aimbotSmoothingFactor, 9, function(value)
    aimbotSmoothingFactor = value
end)

local mouseStrengthSlider = createAimbotSlider("Força da Mira (Mouse)", 1, 30, mouseAimbotStrength, 10, function(value)
    mouseAimbotStrength = value
end)

-- CORRIGIDO: Seletor de parte do corpo agora atualiza a variável global corretamente
createAimbotSelector("Parte Alvo", {"Head", "Torso", "HumanoidRootPart", "UpperTorso", "LowerTorso", "LeftFoot", "RightFoot", "LeftHand", "RightHand", "Left Arm", "Right Arm", "Left Leg", "Right Leg"}, 11, function(value)
    aimbotTargetPart = value
    print("Aimbot parte alvo mudada para: " .. aimbotTargetPart)
end)

-- Slider de Prediction
createAimbotSlider("Prediction", 0, 50, 15, 12, function(value)
    aimbotPrediction = value / 100
    print("Aimbot prediction: " .. aimbotPrediction .. "s")
end)

createAimbotSelector("Tecla de Ativação", {"Botão Mouse 2", "CTRL Esquerdo"}, 12, function(value)
    if value == "Botão Mouse 2" then
        aimbotActivationKey = "Mouse2"
    elseif value == "CTRL Esquerdo" then
        aimbotActivationKey = "LeftControl"
    end
end)

createAimbotSelector("Modo do Aimbot", {"Câmera", "Mouse"}, 13, function(value)
    if value == "Câmera" then
        aimbotMode = "Câmera"
        cameraSmoothSlider.Visible = true
        mouseStrengthSlider.Visible = false
    elseif value == "Mouse" then
        aimbotMode = "Mouse"
        cameraSmoothSlider.Visible = false
        mouseStrengthSlider.Visible = true
    end
end)

cameraSmoothSlider.Visible = true
mouseStrengthSlider.Visible = false

--[[============================================================
    UI DO SILENT AIM
============================================================]]--

-- Divisor visual
local SilentAimDivider = Instance.new("Frame", AimbotPage)
SilentAimDivider.Size = UDim2.new(1, -40, 0, 2)
SilentAimDivider.BackgroundColor3 = Theme.Stroke
SilentAimDivider.BorderSizePixel = 0
SilentAimDivider.LayoutOrder = 14
local DividerGradient = Instance.new("UIGradient", SilentAimDivider)
DividerGradient.Color = ColorSequence.new({
    ColorSequenceKeypoint.new(0, Theme.Stroke),
    ColorSequenceKeypoint.new(0.5, Theme.Accent),
    ColorSequenceKeypoint.new(1, Theme.Stroke)
})

-- Título da seção Silent Aim
local SilentAimSectionTitle = Instance.new("TextLabel", AimbotPage)
SilentAimSectionTitle.Text = "SILENT AIM"
SilentAimSectionTitle.Size = UDim2.new(1, -40, 0, 35)
SilentAimSectionTitle.BackgroundTransparency = 1
SilentAimSectionTitle.Font = Enum.Font.SourceSansSemibold
SilentAimSectionTitle.TextColor3 = Theme.Accent
SilentAimSectionTitle.TextSize = 20
SilentAimSectionTitle.TextXAlignment = Enum.TextXAlignment.Left
SilentAimSectionTitle.LayoutOrder = 15

local SilentAimDesc = Instance.new("TextLabel", AimbotPage)
SilentAimDesc.Text = "Acerta automaticamente no alvo mais próximo ao atirar, sem mover a câmera ou cursor."
SilentAimDesc.Size = UDim2.new(1, -40, 0, 30)
SilentAimDesc.BackgroundTransparency = 1
SilentAimDesc.Font = Enum.Font.SourceSans
SilentAimDesc.TextColor3 = Theme.TextSecondary
SilentAimDesc.TextSize = 14
SilentAimDesc.TextXAlignment = Enum.TextXAlignment.Left
SilentAimDesc.TextWrapped = true
SilentAimDesc.LayoutOrder = 16

-- Toggle do Silent Aim
local updateSilentAimToggle = createAimbotToggle("Silent Aim", 17, function(update)
    silentAimEnabled = not silentAimEnabled
    update(silentAimEnabled)
end)
updateSilentAimToggle(silentAimEnabled)

-- Slider de Chance de Acerto
createAimbotSlider("Chance de Acerto (%)", 0, 100, silentAimHitChance, 18, function(value)
    silentAimHitChance = value
end)

--[[============================================================
    SISTEMA DE AMIGOS - LÓGICA E FUNÇÕES
============================================================]]--

-- Função para adicionar um amigo
local function addFriend(playerName)
    friendsList[playerName] = true
    print("Amigo adicionado: " .. playerName)
    
    -- Atualiza cor do ESP se já existir
    local player = Players:FindFirstChild(playerName)
    if player and ESPObjects[player] and ESPObjects[player].Label then
        ESPObjects[player].Label.TextColor3 = Color3.fromRGB(34, 197, 94)
    end
end

-- Função para remover um amigo
local function removeFriend(playerName)
    friendsList[playerName] = nil
    print("Amigo removido: " .. playerName)
    
    -- Atualiza cor do ESP se existir
    local player = Players:FindFirstChild(playerName)
    if player and ESPObjects[player] and ESPObjects[player].Label then
        ESPObjects[player].Label.TextColor3 = Color3.fromRGB(255, 255, 255)
    end
    
    -- Remove da UI se não estiver próximo
    if nearbyPlayersUI[playerName] then
        local char = player and player.Character
        local hrp = char and char:FindFirstChild("HumanoidRootPart")
        local myChar = Player.Character
        local myHrp = myChar and myChar:FindFirstChild("HumanoidRootPart")
        
        if not hrp or not myHrp or (hrp.Position - myHrp.Position).Magnitude > proximityRadius then
            if nearbyPlayersUI[playerName] then
                nearbyPlayersUI[playerName]:Destroy()
                nearbyPlayersUI[playerName] = nil
            end
        end
    end
end

-- Função para criar UI de um jogador na lista
local function createPlayerUI(playerName, isFriend)
    if nearbyPlayersUI[playerName] then return end
    
    local PlayerFrame = Instance.new("Frame", NearbyScrollFrame)
    PlayerFrame.Name = playerName
    PlayerFrame.Size = UDim2.new(1, -10, 0, 35)
    PlayerFrame.BackgroundColor3 = isFriend and Color3.fromRGB(22, 163, 74) or Theme.Primary
    local PFrameCorner = Instance.new("UICorner", PlayerFrame)
    PFrameCorner.CornerRadius = UDim.new(0, 6)
    
    local PlayerNameBtn = Instance.new("TextButton", PlayerFrame)
    PlayerNameBtn.Name = "NameButton"
    PlayerNameBtn.Text = playerName
    PlayerNameBtn.Size = UDim2.new(1, isFriend and -80 or -10, 1, 0)
    PlayerNameBtn.Position = UDim2.new(0, 5, 0, 0)
    PlayerNameBtn.BackgroundTransparency = 1
    PlayerNameBtn.Font = Enum.Font.SourceSans
    PlayerNameBtn.TextColor3 = Theme.Text
    PlayerNameBtn.TextSize = 14
    PlayerNameBtn.TextXAlignment = Enum.TextXAlignment.Left
    
    if not isFriend then
        -- Adicionar amigo ao clicar
        PlayerNameBtn.MouseButton1Click:Connect(function()
            addFriend(playerName)
            -- Recria a UI para mostrar o botão de remover
            PlayerFrame:Destroy()
            nearbyPlayersUI[playerName] = nil
            createPlayerUI(playerName, true)
        end)
        
        CreateButtonHover(PlayerNameBtn, Theme.Secondary, Color3.fromRGB(0, 0, 0, 0))
    else
        -- Botão para remover amigo
        local RemoveBtn = Instance.new("TextButton", PlayerFrame)
        RemoveBtn.Text = "X"
        RemoveBtn.Size = UDim2.new(0, 30, 0, 25)
        RemoveBtn.Position = UDim2.new(1, -70, 0.5, -12.5)
        RemoveBtn.BackgroundColor3 = Theme.Error
        RemoveBtn.Font = Enum.Font.SourceSansBold
        RemoveBtn.TextColor3 = Theme.Text
        RemoveBtn.TextSize = 14
        local RemoveBtnCorner = Instance.new("UICorner", RemoveBtn)
        RemoveBtnCorner.CornerRadius = UDim.new(0, 4)
        
        RemoveBtn.MouseButton1Click:Connect(function()
            removeFriend(playerName)
            PlayerFrame:Destroy()
            nearbyPlayersUI[playerName] = nil
            
            -- Recria a UI se o jogador ainda estiver próximo
            local player = Players:FindFirstChild(playerName)
            if player then
                local char = player.Character
                local hrp = char and char:FindFirstChild("HumanoidRootPart")
                local myChar = Player.Character
                local myHrp = myChar and myChar:FindFirstChild("HumanoidRootPart")
                
                if hrp and myHrp and (hrp.Position - myHrp.Position).Magnitude <= proximityRadius then
                    createPlayerUI(playerName, false)
                end
            end
        end)
        
        CreateButtonHover(RemoveBtn, Color3.fromRGB(220, 38, 38), Theme.Error)
    end
    
    nearbyPlayersUI[playerName] = PlayerFrame
end

-- Loop para atualizar jogadores próximos
task.spawn(function()
    while task.wait(0.5) do
        if not Player.Character then continue end
        local myHrp = Player.Character:FindFirstChild("HumanoidRootPart")
        if not myHrp then continue end
        
        local nearbyPlayers = {}
        
        -- Detecta jogadores próximos
        for _, player in ipairs(Players:GetPlayers()) do
            if player ~= Player then
                local char = player.Character
                local hrp = char and char:FindFirstChild("HumanoidRootPart")
                
                if hrp then
                    local distance = (hrp.Position - myHrp.Position).Magnitude
                    if distance <= proximityRadius then
                        nearbyPlayers[player.Name] = true
                        
                        -- Cria UI se não existir
                        if not nearbyPlayersUI[player.Name] then
                            createPlayerUI(player.Name, friendsList[player.Name] or false)
                        end
                    end
                end
            end
        end
        
        -- Remove jogadores que se afastaram (exceto amigos)
        for playerName, frame in pairs(nearbyPlayersUI) do
            if not nearbyPlayers[playerName] and not friendsList[playerName] then
                frame:Destroy()
                nearbyPlayersUI[playerName] = nil
            end
        end
        
        -- Atualiza cores dos frames de amigos
        for playerName, _ in pairs(friendsList) do
            if nearbyPlayersUI[playerName] then
                nearbyPlayersUI[playerName].BackgroundColor3 = Color3.fromRGB(22, 163, 74)
            end
        end
    end
end)

-- CORRIGIDO: Loop principal do Aimbot agora usa aimbotTargetPart corretamente
RunService.RenderStepped:Connect(function()
    -- CORRIGIDO: FOV agora é visível independente do aimbot estar ativado
    local mouseLocation = UserInputService:GetMouseLocation()
    
    -- Atualiza posição e visibilidade do FOV
    fovCircle.Visible = aimbotShowFov
    
    if fovCircle.Visible then
        local newSize = aimbotFovRadius * 2
        fovCircle.Size = UDim2.fromOffset(newSize, newSize)
        fovCircle.Position = UDim2.fromOffset(mouseLocation.X, mouseLocation.Y)
    end
    
    --[[============================================================
        LÓGICA DO AIMBOT NORMAL
    ============================================================]]--
    -- Se o aimbot não está ativado, não faz nada além de mostrar o FOV
    if not aimbotEnabled then
        currentAimbotTarget = nil
        return
    end
    
    -- CORRIGIDO: Sempre usa a posição do mouse como ponto de referência
    local aimPoint = mouseLocation

    if isAimKeyPressed() then
        local isTargetValid = false
        if currentAimbotTarget and currentAimbotTarget.Parent then
            local humanoid = currentAimbotTarget:FindFirstChildOfClass("Humanoid")
            if humanoid and humanoid.Health > 0 then
                -- MELHORADO: Usa detecção automática de partes
                local targetPart = getBestTargetPart(currentAimbotTarget)
                if targetPart and isVisible(targetPart) then
                    -- Verifica se o alvo ainda está dentro do FOV com prediction
                    local predictedPos = getPredictedPosition(targetPart)
                    local targetScreenPos = Camera:WorldToViewportPoint(predictedPos)
                    local distanceFromAim = (Vector2.new(targetScreenPos.X, targetScreenPos.Y) - aimPoint).Magnitude

                    if distanceFromAim <= aimbotFovRadius then
                        isTargetValid = true
                    end
                end
            end
        end

        if not isTargetValid then
            local newTargetPart = getClosestPartToPoint(aimPoint)
            currentAimbotTarget = newTargetPart and newTargetPart.Parent
        end

        if currentAimbotTarget then
            -- MELHORADO: Usa getBestTargetPart para mirar na parte correta
            local partToAim = getBestTargetPart(currentAimbotTarget)
            if partToAim then
                if aimbotMode == "Câmera" then
                    smoothLookAt(partToAim)
                elseif aimbotMode == "Mouse" then
                    moveMouseTowards(partToAim)
                end
            end
        end

    else
        currentAimbotTarget = nil
    end
end)


--[[============================================================
    CONTROLES DO HUB (ABRIR/FECHAR)
============================================================]]--
local function ToggleHub(forceState)
    HubVisible = (forceState ~= nil) and forceState or not HubVisible
    
    local goalSize = HubVisible and UDim2.new(0, 800, 0, 500) or UDim2.new(0, 800, 0, 0)
    local goalTransparency = HubVisible and 0 or 1
    
    if HubVisible then
        MainFrame.Visible = true
    end
    
    local tween = TweenService:Create(MainFrame, AnimationInfo.Medium, {Size = goalSize})
    local fadeTween = TweenService:Create(MainFrame, AnimationInfo.Medium, {BackgroundTransparency = goalTransparency})
    
    tween:Play()
    fadeTween:Play()
    
    if not HubVisible then
        tween.Completed:Connect(function()
            MainFrame.Visible = false
        end)
    end
end

local function CloseHub()
    ToggleHub(false)
    task.wait(0.4)
    ScreenGui:Destroy()
end

UserInputService.InputBegan:Connect(function(input, gameProcessed)
    if not gameProcessed and input.KeyCode == Enum.KeyCode.H then
        ToggleHub()
    elseif not gameProcessed and input.KeyCode == Enum.KeyCode.V then
        aimbotEnabled = not aimbotEnabled
        updateAimbotToggle(aimbotEnabled)
        
        local NotifFrame = Instance.new("Frame", ScreenGui)
        NotifFrame.Size = UDim2.new(0, 250, 0, 50)
        NotifFrame.Position = UDim2.new(1, -270, 1, -70)
        NotifFrame.BackgroundColor3 = Theme.Primary
        local c = Instance.new("UICorner", NotifFrame); c.CornerRadius = UDim.new(0, 8)
        local s = Instance.new("UIStroke", NotifFrame); s.Color = Theme.Accent; s.Thickness = 1.5
        local t = Instance.new("TextLabel", NotifFrame)
        t.RichText = true
        t.Text = "Aimbot: " .. (aimbotEnabled and "<font color='#4ade80'>ATIVADO</font>" or "<font color='#f87171'>DESATIVADO</font>")
        t.Size = UDim2.new(1, 0, 1, 0)
        t.BackgroundTransparency = 1
        t.Font = Enum.Font.SourceSansBold
        t.TextColor3 = Theme.Text
        t.TextSize = 16
        
        Debris:AddItem(NotifFrame, 2.5)
        TweenService:Create(NotifFrame, AnimationInfo.Fast, {Position = UDim2.new(1, -270, 1, -130)}):Play()
        task.wait(2)
        TweenService:Create(NotifFrame, AnimationInfo.Fast, {Position = UDim2.new(1, -270, 1, -70)}):Play()
    end
end)
CloseButton.MouseButton1Click:Connect(CloseHub)
CreateButtonHover(CloseButton, Theme.Error, Theme.Primary)

--[[============================================================
    ANIMAÇÕES DECORATIVAS ADICIONAIS
============================================================]]--
task.spawn(function()
    while task.wait() do
        if MainFrame.Visible then
            local tween1 = TweenService:Create(TitleGradient, AnimationInfo.Slow, {Offset = Vector2.new(0.5, 0)})
            local tween2 = TweenService:Create(TitleGradient, AnimationInfo.Slow, {Offset = Vector2.new(-0.5, 0)})
            tween1:Play()
            tween1.Completed:Wait()
            tween2:Play()
            tween2.Completed:Wait()
        end
    end
end)

task.spawn(function()
    local originalColor = Theme.Success
    local brighterColor = originalColor:Lerp(Color3.new(1, 1, 1), 0.2)
    while task.wait(0.1) do
        if ESPEnabled and MainFrame.Visible then
            local tweenUp = TweenService:Create(ESPToggle, TweenInfo.new(1), {BackgroundColor3 = brighterColor})
            local tweenDown = TweenService:Create(ESPToggle, TweenInfo.new(1), {BackgroundColor3 = originalColor})
            tweenUp:Play()
            tweenUp.Completed:Wait()
            tweenDown:Play()
            tweenDown.Completed:Wait()
        else
            task.wait(0.5)
        end
    end
end)

--[[============================================================
    INICIALIZAÇÃO E NOTIFICAÇÃO
============================================================]]--
local function ShowNotification()
    local NotifFrame = Instance.new("Frame", ScreenGui)
    NotifFrame.Size = UDim2.new(0, 300, 0, 60)
    NotifFrame.Position = UDim2.new(0.5, -150, 1, 80)
    NotifFrame.BackgroundColor3 = Theme.Primary
    
    local NotifCorner = Instance.new("UICorner", NotifFrame)
    NotifCorner.CornerRadius = UDim.new(0, 8)
    local NotifStroke = Instance.new("UIStroke", NotifFrame)
    NotifStroke.Color = Theme.Accent
    NotifStroke.Thickness = 1.5
    
    local NotifText = Instance.new("TextLabel", NotifFrame)
    NotifText.RichText = true
    NotifText.Text = string.format("<b><font color='#%s'>VersaTools</font></b> carregado! Pressione <b>H</b> para abrir.", Theme.Accent:ToHex())
    NotifText.Size = UDim2.new(1, -20, 1, 0)
    NotifText.Position = UDim2.new(0, 10, 0, 0)
    NotifText.BackgroundTransparency = 1
    NotifText.Font = Enum.Font.SourceSans
    NotifText.TextColor3 = Theme.Text
    NotifText.TextSize = 14
    NotifText.TextWrapped = true
    
    TweenService:Create(NotifFrame, AnimationInfo.Medium, {Position = UDim2.new(0.5, -150, 1, -80)}):Play()
    task.wait(3.5)
    local tweenOut = TweenService:Create(NotifFrame, AnimationInfo.Medium, {Position = UDim2.new(0.5, -150, 1, 80)})
    tweenOut:Play()
    tweenOut.Completed:Connect(function() NotifFrame:Destroy() end)
end

-- Inicializar
ShowNotification()
ShowPage(DashboardPage, DashboardBtn)
ToggleHub(true)



-- ========================================
-- LÓGICA REWIND E BALL MODE
-- ========================================

-- Rewind
local function startRewind()
    rewindEnabled = true
    rewindPositions = {}
    
    rewindConnection = RunService.Heartbeat:Connect(function()
        if not rewindActive and Player.Character then
            local hrp = Player.Character:FindFirstChild("HumanoidRootPart")
            if hrp then
                table.insert(rewindPositions, 1, hrp.CFrame)
                if #rewindPositions > maxRewindPositions then
                    table.remove(rewindPositions)
                end
            end
        end
    end)
    
    rewindInputConnection = UserInputService.InputBegan:Connect(function(input, gameProcessed)
        if gameProcessed or not rewindEnabled then return end
        
        if input.KeyCode == Enum.KeyCode.C and not rewindActive then
            rewindActive = true
            
            local currentIndex = 1
            local char = Player.Character
            if not char then return end
            
            local hrp = char:FindFirstChild("HumanoidRootPart")
            local humanoid = char:FindFirstChildOfClass("Humanoid")
            
            if not hrp or not humanoid then return end
            
            humanoid.PlatformStand = true
            
            rewindUpdateConnection = RunService.Heartbeat:Connect(function()
                if not UserInputService:IsKeyDown(Enum.KeyCode.C) or not rewindEnabled then
                    rewindActive = false
                    humanoid.PlatformStand = false
                    
                    if rewindUpdateConnection then
                        rewindUpdateConnection:Disconnect()
                        rewindUpdateConnection = nil
                    end
                    return
                end
                
                if currentIndex <= #rewindPositions then
                    local targetCFrame = rewindPositions[currentIndex]
                    hrp.CFrame = targetCFrame
                    hrp.Velocity = Vector3.zero
                    hrp.RotVelocity = Vector3.zero
                    currentIndex = currentIndex + 1
                else
                    rewindActive = false
                    humanoid.PlatformStand = false
                    
                    if rewindUpdateConnection then
                        rewindUpdateConnection:Disconnect()
                        rewindUpdateConnection = nil
                    end
                end
            end)
        end
    end)
end

local function stopRewind()
    rewindEnabled = false
    rewindActive = false
    
    if rewindConnection then
        rewindConnection:Disconnect()
        rewindConnection = nil
    end
    
    if rewindInputConnection then
        rewindInputConnection:Disconnect()
        rewindInputConnection = nil
    end
    
    if rewindUpdateConnection then
        rewindUpdateConnection:Disconnect()
        rewindUpdateConnection = nil
    end
    
    if Player.Character then
        local humanoid = Player.Character:FindFirstChildOfClass("Humanoid")
        if humanoid then
            humanoid.PlatformStand = false
        end
    end
    
    rewindPositions = {}
end

RewindToggle.MouseButton1Click:Connect(function()
    rewindEnabled = not rewindEnabled
    RewindToggle.Text = "Rewind (Hold C): " .. (rewindEnabled and "ATIVADO" or "DESATIVADO")
    RewindToggle.BackgroundColor3 = rewindEnabled and Theme.Success or Theme.Error
    
    if rewindEnabled then
        startRewind()
    else
        stopRewind()
    end
end)

-- Ball Mode
local function enableBallMode()
    local char = Player.Character or Player.CharacterAdded:Wait()
    local humanoid = char:WaitForChild("Humanoid")
    local root = char:WaitForChild("HumanoidRootPart")
    
    for _, part in ipairs(char:GetDescendants()) do
        if part:IsA("BasePart") then
            part.CanCollide = false
        end
    end
    
    root.Shape = Enum.PartType.Ball
    root.Size = Vector3.new(5, 5, 5)
    
    local params = RaycastParams.new()
    params.FilterType = Enum.RaycastFilterType.Blacklist
    params.FilterDescendantsInstances = {char}
    
    ballConnection = RunService.RenderStepped:Connect(function(delta)
        if not root or not humanoid or humanoid.Health <= 0 then return end
        root.CanCollide = true
        humanoid.PlatformStand = true
        
        if UserInputService:GetFocusedTextBox() then return end
        
        local move = Vector3.zero
        if UserInputService:IsKeyDown(Enum.KeyCode.W) then move -= Workspace.CurrentCamera.CFrame.RightVector end
        if UserInputService:IsKeyDown(Enum.KeyCode.A) then move -= Workspace.CurrentCamera.CFrame.LookVector end
        if UserInputService:IsKeyDown(Enum.KeyCode.S) then move += Workspace.CurrentCamera.CFrame.RightVector end
        if UserInputService:IsKeyDown(Enum.KeyCode.D) then move += Workspace.CurrentCamera.CFrame.LookVector end
        
        if move.Magnitude > 0 then
            root.RotVelocity += move.Unit * delta * ballSpeed
        end
    end)
    
    ballJumpConnection = UserInputService.JumpRequest:Connect(function()
        local result = workspace:Raycast(root.Position, Vector3.new(0, -((root.Size.Y / 2) + 0.3), 0), params)
        if result then
            root.Velocity = root.Velocity + Vector3.new(0, ballJumpPower, 0)
        end
    end)
    
    Workspace.CurrentCamera.CameraSubject = root
end

local function disableBallMode()
    local char = Player.Character
    if not char then return end
    
    local root = char:FindFirstChild("HumanoidRootPart")
    if root then
        root.CFrame = CFrame.new(root.Position)
        root.AssemblyLinearVelocity = Vector3.zero
        root.AssemblyAngularVelocity = Vector3.zero
        root.Shape = Enum.PartType.Block
        root.Size = Vector3.new(2, 2, 1)
        root.CanCollide = true
    end
    
    local humanoid = char:FindFirstChildOfClass("Humanoid")
    if humanoid then
        humanoid.PlatformStand = false
        humanoid:ChangeState(Enum.HumanoidStateType.GettingUp)
        Workspace.CurrentCamera.CameraSubject = humanoid
    end
    
    if ballConnection then ballConnection:Disconnect(); ballConnection = nil end
    if ballJumpConnection then ballJumpConnection:Disconnect(); ballJumpConnection = nil end
end

BallModeToggle.MouseButton1Click:Connect(function()
    ballModeEnabled = not ballModeEnabled
    BallModeToggle.Text = "Ball Mode: " .. (ballModeEnabled and "ATIVADO" or "DESATIVADO")
    BallModeToggle.BackgroundColor3 = ballModeEnabled and Theme.Success or Theme.Error
    
    if ballModeEnabled then
        enableBallMode()
    else
        disableBallMode()
    end
end)


print("VersaTools Hub 3.3 (Modificado - Aimbot Corrigido) carregado!")
print("Pressione H para abrir/fechar.")
print("Pressione V para ativar/desativar o Aimbot.")