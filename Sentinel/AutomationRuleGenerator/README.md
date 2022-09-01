# 自動生成分析規則


## 安裝相關套件

- [安裝powershell](https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.2#msi)

- 安裝Azure powershell module

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Install-Module -Name Az -Scope CurrentUser -Repository PSGallery -Force
Install-Module -Name Az.SecurityInsights -RequiredVersion 1.0.0
```

## 下載規則範本

- 開啟windows powershell並使用Azure模組登入以及連線
- 產生`templates.json`

```powershell
Connect-AzAccount -TenantID .....
$AlertRuleTemplates = Get-AzSentinelAlertRuleTemplate -ResourceGroupName "MyResourceGroup" -WorkspaceName "MyWorkspaceName"
$template_json = ConvertTo-Json($AlertRuleTemplates)
echo $template_json >　templates.json
```

## 列舉現有資料來源

- 到要導入分析規則的Sentinel所使用的log analytics列舉所有Data Source 
    - 儲存為**query_data.csv**
```Kusto
search *
| distinct $table
| sort by $table asc nulls last
```





## 生成要導入到Sentinel的CSV

### 概述

- 依據DataSources生成template
- 規則類別有三種Scheduled、Fusion、MicrosoftSecurityIncidentCreation
  - 每種import的powershell語法不同
  - **實際上只有 Scheduled的最多**，其他少的幾乎可以忽略，這邊就只實作Scheduled類別的

### 步驟

- 將query_data.csv、templates.json與[generate_rule_csv.py](Sentinel\AutomationRuleGenerator\generate_rule_csv.py)放在同一個資料夾
- 運行[generate_rule_csv.py](Sentinel\AutomationRuleGenerator\generate_rule_csv.py)
- 生成 Scheduled.csv


## 使用Powershell將生成規則導入Sentinel

- 將Scheduled.csv和[import_rule_to_sentinel.ps1](Sentinel\AutomationRuleGenerator\import_rule_to_sentinel.ps1)放在同一個資料夾
- 開啟powershell並用Azure的模組登入後，運行 `.\import_rule_to_sentinel.ps1`








## Reference


FROM:

https://adamtheautomator.com/import-csv-foreach/
https://docs.microsoft.com/en-us/powershell/module/az.securityinsights/new-azsentinelalertrule?view=azps-8.0.0

REF:
https://www.garybushey.com/2020/01/11/your-first-azure-sentinel-rest-api-call/
https://www.garybushey.com/2020/01/12/working-with-analytics-rules-part-1-templates/
https://www.garybushey.com/2020/02/01/create-multiple-azure-sentinel-rules-from-selected-templates/