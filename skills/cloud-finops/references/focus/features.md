<!-- Source: FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec (Community Specification License 1.0) -->

# Account Structures

## Description

Different service providers have different account constructs that FinOps practitioners use for allocation, reporting, and more. Organizations may have one or many accounts within one or more service providers and FinOps practitioners may need to review the cost broken down by each account. FOCUS has two types of accounts: a billing account and a sub account.

A billing account is the account where invoices are generated. Each billing account can have one or more sub accounts, which can be used for deploying and managing resources and services. Billing and sub accounts are often used to facilitate allocation strategies and FinOps practitioners must be able to break costs down by billing and sub account to facilitate FinOps scenarios like chargeback and budgeting.

## Directly Dependent Columns

* BilledCost
* BillingAccountId
* BillingAccountName
* BillingAccountType
* SubAccountId
* SubAccountName
* SubAccountType

## Supporting Columns

* InvoiceId

## Example SQL Query

```sql
SELECT
  BillingAccountId,
  BillingAccountName,
  BillingAccountType,
  SubAccountId,
  SubAccountName,
  SubAccountType,
  SUM(BilledCost)
FROM focus_data_table
WHERE BillingPeriodStart >= ? AND BillingPeriodEnd < ?
GROUP BY
  BillingAccountId,
  SubAccountId
```

## Introduced (Version)

0.5

---

# Billed Cost and Invoice Alignment

## Description

FOCUS data should be consistent with the costs indicated on payable invoices. This is relevant to the total cost of the invoice, as well as the period of time the invoice covers.

## Directly Dependent Columns

* BilledCost
* BillingCurrency
* BillingPeriodEnd
* BillingPeriodStart
* InvoiceId

## Supporting Columns

* ServiceName

## Example SQL Query

```sql
SELECT
  BillingPeriodStart,
  BillingPeriodEnd,
  InvoiceId,
  SUM(BilledCost)
FROM focus_data_table
GROUP BY
  BillingPeriodStart,
  BillingPeriodEnd,
  InvoiceId
```

## Introduced (Version)

0.5

---

# Charge Categorization

## Description

FOCUS supports the categorization of charges including purchases, usage, tax, credits and adjustments. It includes classification on frequency. It includes classification on correction vs normal entries.

## Directly Dependent Columns

* ChargeCategory
* ChargeClass
* ChargeFrequency

## Supporting Columns

* BilledCost
* BillingAccountId
* BillingPeriodEnd
* BillingPeriodStart
* CommitmentDiscountId
* CommitmentDiscountType
* ServiceProviderName
* ServiceCategory

## Example SQL Query

### Report on Commitment Discount Purchases

```sql
SELECT
  MIN(ChargePeriodStart) AS ChargePeriodStart,
  MAX(ChargePeriodEnd) AS ChargePeriodEnd,
  ServiceProviderName,
  BillingAccountId,
  CommitmentDiscountId,
  CommitmentDiscountType,
  CommitmentDiscountUnit,
  CommitmentDiscountQuantity,
  ChargeFrequency,
  SUM(BilledCost) AS TotalBilledCost
FROM focus_data_table
WHERE ChargePeriodStart >= ? AND ChargePeriodEnd < ?
  AND ChargeCategory = 'Purchase'
  AND CommitmentDiscountId IS NOT NULL
GROUP BY
  ServiceProviderName,
  BillingAccountId,
  CommitmentDiscountId,
  CommitmentDiscountType,
  CommitmentDiscountUnit,
  CommitmentDiscountQuantity,
  ChargeFrequency
```

### Report on Corrections

```sql
SELECT
  ServiceProviderName,
  BillingAccountId,
  ChargeCategory,
  ServiceCategory,
  ServiceName,
  SUM(BilledCost) AS TotalBilledCost
FROM focus_data_table
WHERE BillingPeriodStart >= ? AND BillingPeriodEnd < ?
  AND ChargeClass = 'Correction'
GROUP BY
  ServiceProviderName,
  BillingAccountId,
  ChargeCategory,
  ServiceCategory,
  ServiceName
```

### Report Recurring Charges

```sql
SELECT
  BillingPeriodStart,
  CommitmentDiscountId,
  CommitmentDiscountName,
  CommitmentDiscountType,
  ChargeFrequency,
  SUM(BilledCost) AS TotalBilledCost
FROM focus_data_table
WHERE BillingPeriodStart  >= ? AND BillingPeriodStart < ?
  AND ChargeFrequency = 'Recurring'
  AND CommitmentDiscountId IS NOT NULL
GROUP BY
  BillingPeriodStart,
  CommitmentDiscountId,
  CommitmentDiscountName,
  CommitmentDiscountType,
  ChargeFrequency
```

## Introduced (Version)

1.0

---

# Commit Usage and Under Usage

## Description

FOCUS supports the tracking of commitment discounts usage and under usage, which can come in the form of commitment discounts or capacity reservations.

## Directly Dependent Columns

* CommitmentDiscountID
* CommitmentDiscountStatus
* CommitmentDiscountType
* CapacityReservationID
* CapacityReservationStatus
* CapacityReservationType

## Supporting Columns

* BilledCost
* ChargePeriodStart
* ChargePeriodEnd
* EffectiveCost
* ServiceCategory

## Example SQL Query for Commitment Discounts

```sql
SELECT
  ServiceProviderName,
  BillingAccountId,
  CommitmentDiscountId,
  CommitmentDiscountType,
  CommitmentDiscountStatus,
  SUM(BilledCost) AS TotalBilledCost,
  SUM(EffectiveCost) AS TotalEffectiveCost
FROM focus_data_table
WHERE ChargePeriodStart >= ? AND ChargePeriodEnd < ?
  AND CommitmentDiscountStatus = 'Unused'
GROUP BY
  ServiceProviderName,
  BillingAccountId,
  CommitmentDiscountId,
  CommitmentDiscountType
```

## Example SQL Query for Capacity Reservations

```sql
SELECT
  ServiceProviderName,
  BillingAccountId,
  CapacityReservationId,
  CapacityReservationStatus,
  SUM(BilledCost) AS TotalBilledCost,
  SUM(EffectiveCost) AS TotalEffectiveCost
FROM focus_data_table
WHERE ChargePeriodStart >= ? AND ChargePeriodEnd < ?
  AND CapacityReservationStatus = 'Unused'
GROUP BY
  ServiceProviderName,
  BillingAccountId,
  CapacityReservationId,
  CapacityReservationStatus
```

## Introduced (Version)

1.0

---

# Contract Commitments

## Description

FOCUS supports the tracking of commitments made via contractual agreements between a service provider and a customer. Each row in the Cost and Usage dataset is associated with one or more unique identifiers representing those contracts and contract commitments, stored in a JSON column called Contract Applied. A richer amount of detail that describes those commitments is carried in a separate Contract Commitment dataset, which can be joined to the Cost and Usage dataset to facilitate various queries involving filtering and aggregation.

The Contract Applied column contains several FOCUS-defined properties.  For more information, see the definition of Contract Applied here.

## Directly Dependent Columns

* CostAndUsage
  * ContractApplied

## Supporting Columns

* ContractCommitment
  * BillingCurrency
  * ContractCommitmentCategory
  * ContractCommitmentCost
  * ContractCommitmentDescription
  * ContractCommitmentId
  * ContractCommitmentPeriodEnd
  * ContractCommitmentPeriodStart
  * ContractCommitmentQuantity
  * ContractCommitmentType
  * ContractCommitmentUnit
  * ContractId
  * ContractPeriodEnd
  * ContractPeriodStart

## Example SQL Queries

The FOCUS specification implements the application of contract commitments to cost and usage via the *ContractApplied* column, which is defined in *JSON object format*.

Because ANSI SQL does not inherently support the parsing of JSON, the following queries leverage the JSON functions found in BigQuery Standard SQL in order to demonstrate this feature's functionality.  Similar JSON functions are available in all major SQL engines; thus, the below examples can be slightly modified to accommodate any particular database instance.

### Report on Initial Contract Commitment

This query takes inputs of a time range via ChargePeriodStart and ChargePeriodEnd, then presents the aggregation of initial contract commitments from the CostAndUsage dataset per ServiceProviderName and ContractCommitmentID by filtering on the specified time range, along with ChargeCategory of `Purchase`.

```sql
SELECT
  MIN(CU.ChargePeriodStart) AS ChargePeriodStart,
  MAX(CU.ChargePeriodEnd) AS ChargePeriodEnd,
  CU.ServiceProviderName,
  JSON_VALUE(CA, '$.ContractCommitmentID') AS ContractCommitmentId,
  SUM(CAST(JSON_VALUE(CA, '$.ContractCommitmentAppliedCost') AS FLOAT64)) AS ContractCommitmentAppliedCost
FROM CostAndUsage CU
CROSS JOIN
  UNNEST(JSON_EXTRACT_ARRAY(CU.ContractApplied, '$.Elements')) AS CA
WHERE JSON_VALUE(CA, '$.ContractCommitmentAppliedCost') IS NOT NULL
  AND ChargePeriodStart >= ? AND ChargePeriodEnd < ?
  AND ChargeCategory = 'Purchase'
GROUP BY ServiceProviderName, ContractCommitmentId
ORDER BY ServiceProviderName, ContractCommitmentId
```

### Report on Usage Against Contract Commitment

This query takes inputs of a time range via ChargePeriodStart and ChargePeriodEnd, then presents the aggregation of the application of contract commitments from the CostAndUsage dataset per ServiceProviderName and ContractCommitmentID by filtering on the specified time range, along with ChargeCategory of `Usage`.

```sql
SELECT
  MIN(CU.ChargePeriodStart) AS ChargePeriodStart,
  MAX(CU.ChargePeriodEnd) AS ChargePeriodEnd,
  CU.ServiceProviderName,
  JSON_VALUE(CA, '$.ContractCommitmentID') AS ContractCommitmentId,
  SUM(CAST(JSON_VALUE(CA, '$.ContractCommitmentAppliedCost') AS FLOAT64)) AS ContractCommitmentAppliedCost
FROM CostAndUsage CU
CROSS JOIN
  UNNEST(JSON_EXTRACT_ARRAY(CU.ContractApplied, '$.Elements')) AS CA
WHERE JSON_VALUE(CA, '$.ContractCommitmentAppliedCost') IS NOT NULL
  AND ChargePeriodStart >= ? AND ChargePeriodEnd < ?
  AND ChargeCategory = 'Usage'
GROUP BY ServiceProviderName, ContractCommitmentId
ORDER BY ServiceProviderName, ContractCommitmentId
```

### Report on Usage Against Contract Commitment by Category

This query takes inputs of a time range via ChargePeriodStart and ChargePeriodEnd, then presents the aggregation of the application of contract commitments from the CostAndUsage dataset per ServiceProviderName and ContractCommitmentID by filtering on the specified time range, along with ChargeCategory of `Usage`.  It also joins in the ContractCommitment dataset to provide further information about each contract commitment (in this case, the start and end date/time).

```sql
SELECT
  MIN(CU.ChargePeriodStart) AS ChargePeriodStart,
  MAX(CU.ChargePeriodEnd) AS ChargePeriodEnd,
  CU.ServiceProviderName,
  JSON_VALUE(CA, '$.ContractCommitmentID') AS ContractCommitmentId,
  CC.ContractCommitmentPeriodStart,
  CC.ContractCommitmentPeriodEnd,
  SUM(CAST(JSON_VALUE(CA, '$.ContractCommitmentAppliedCost') AS FLOAT64)) AS ContractCommitmentAppliedCost
FROM CostAndUsage CU
CROSS JOIN
  UNNEST(JSON_EXTRACT_ARRAY(CU.ContractApplied, '$.Elements')) AS CA
INNER JOIN
  ContractCommitment CC
ON
  JSON_VALUE(CA, '$.ContractCommitmentID') = CC.ContractCommitmentID
WHERE JSON_VALUE(CA, '$.ContractCommitmentAppliedCost') IS NOT NULL
  AND ChargePeriodStart >= ? AND ChargePeriodEnd < ?
  AND ChargeCategory = 'Usage'
GROUP BY ServiceProviderName, ContractCommitmentId, ContractCommitmentPeriodStart, ContractCommitmentPeriodEnd
ORDER BY ServiceProviderName, ContractCommitmentId, ContractCommitmentPeriodStart, ContractCommitmentPeriodEnd
```

## Introduced (Version)

1.3

---

# Cost and Usage Attribution

## Description

Many service providers have features that allow FinOps practitioners to enrich cost and usage data with metadata that is in addition to service provider defined data, in order to analyze FinOps data using organizational, deployment, or other structures. These features may take the form of directly applied metadata or inherited metadata. FOCUS facilitates the inclusion of this metadata at a row level.

## Directly Dependent Columns

* Tags

## Supporting Columns

* BilledCost
* ConsumedQuantity
* ConsumedUnit
* EffectiveCost

## Example SQL Query

```sql
SELECT
  tags,
  ConsumedUnit,
  SUM(BilledCost),
  SUM(EffectiveCost),
  SUM(ConsumedQuantity)
FROM focus_data_table
WHERE BillingPeriodStart >= ? AND BillingPeriodEnd < ?
GROUP BY
  tags,
  ConsumedUnit
```

## Introduced (Version)

1.0

---

# Cost Comparison

## Description

FOCUS supports the comparison of cost columns in order to identify savings, amortization, or other constructs.

## Directly Dependent Columns

* BilledCost
* ContractedCost
* EffectiveCost
* ListCost

## Supporting Columns

* BillingAccountId
* BillingAccountName
* BillingCurrency
* BillingPeriodEnd
* BillingPeriodStart
* ChargePeriodEnd
* ChargePeriodStart
* ServiceName

## Example SQL Query

```sql
WITH AggregatedData AS (
  SELECT
    ServiceProviderName,
    BillingAccountId,
    BillingAccountName,
    BillingCurrency,
    ServiceName,
    SUM(EffectiveCost) AS TotalEffectiveCost,
    SUM(BilledCost) AS TotalBilledCost,
    SUM(CASE
          WHEN ChargeCategory = 'Usage' AND BilledCost = 0 AND EffectiveCost != 0
          THEN 0
          ELSE ContractedCost
        END) AS TotalContractedCost,
    SUM(CASE
          WHEN ChargeCategory = 'Usage' AND BilledCost = 0 AND EffectiveCost != 0
          THEN 0
          ELSE ListCost
        END) AS TotalListCost
  FROM focus_data_table
  WHERE BillingPeriodStart >= ?
    AND BillingPeriodEnd < ?
    AND ChargeClass IS NULL
  GROUP BY
    ServiceProviderName,
    BillingAccountId,
    BillingAccountName,
    BillingCurrency,
    ServiceName
)
SELECT ServiceProviderName,
    BillingAccountId,
    BillingAccountName,
    BillingCurrency,
    ServiceName,
    TotalEffectiveCost,
    TotalBilledCost,
    TotalListCost,
    1 - (TotalContractedCost / NULLIF(TotalListCost, 0)) * 100 AS ContractedDiscount,
    1 - (TotalEffectiveCost / NULLIF(TotalListCost, 0)) * 100 AS EffectiveDiscount
FROM AggregatedData
```

## Introduced (Version)

0.5

---

# Custom Columns

## Description

FOCUS supports the inclusion of custom columns to facilitate reporting capability that is not covered by the columns included in the specification.

## Directly Dependent Columns

* x_CustomColumn

## Example SQL Query

```sql
SELECT
  BillingPeriodStart,
  x_CustomColumn,
  SUM(BilledCost) AS TotalBilledCost,
FROM focus_data_table
WHERE ServiceName = ?
  AND BillingPeriodStart >= ? AND BillingPeriodStart < ?
GROUP BY
  BillingPeriodStart,
  x_CustomColumn
ORDER BY MonthlyCost DESC
```

## Introduced (Version)

0.5

---

# Data Generator-Calculated Split Cost Allocation

## Description

FOCUS enables tracking of resources split by some internal consumption metrics. This is most common for resources supporting shared usage like compute nodes in a shared cluster (Kubernetes, databases) or storage engines that can share capacity between workloads.

## Directly Dependent Columns

* ResourceId
* EffectiveCost
* BilledCost
* AllocatedResourceId
* AllocatedResourceName
* AllocatedMethodDetails
* AllocatedMethodId

## Supporting Columns

* ChargeCategory
* ChargePeriodEnd
* ChargePeriodStart
* ServiceProviderName
* ServiceName

## Example SQL Query (Find resources with a shared cost)

```sql
SELECT
  DISTINCT ResourceId
FROM focus_data_table
WHERE ChargeCategory='Usage'
  AND ChargePeriodStart >= ? AND ChargePeriodEnd <= ?
  AND AllocatedMethodId IS NOT NULL
```

## Example SQL Query (Get total effective cost by ResourceId (ignore shared cost))

```sql
SELECT
  ResourceId,
  SUM(EffectiveCost) AS TotalEffectiveCost
FROM focus_data_table
WHERE ChargeCategory='Usage'
  AND ChargePeriodStart >= ? AND ChargePeriodEnd <= ?
  AND AllocatedMethodId IS NOT NULL
GROUP BY
  ResourceId
```

## Example SQL Query (Get total effective cost by AllocatedResourceId)

```sql
SELECT
  AllocatedResourceId,
  SUM(EffectiveCost) AS TotalEffectiveCost
FROM focus_data_table
WHERE ChargeCategory='Usage'
  AND ChargePeriodStart >= ? AND ChargePeriodEnd <= ?
  AND AllocatedMethodId IS NOT NULL
GROUP BY
  AllocatedResourceId
```

## Example SQL Query (Find total unallocated split costs by resourceId)

```sql
SELECT
  ResourceId,
  SUM(EffectiveCost) AS TotalEffectiveCost
FROM focus_data_table
WHERE ChargeCategory='Usage'
  AND ChargePeriodStart >= ? AND ChargePeriodEnd <= ?
  AND AllocatedMethodId IS NOT NULL AND AllocatedResourceId IS NULL
GROUP BY
  ResourceId
```

## Example SQL Query (Find how a single resource has been split)

```sql
SELECT
  ResourceId,
  COALESCE(AllocatedResourceId, 'Unallocated') AS AllocatedResourceId,
  SUM(EffectiveCost) AS TotalEffectiveCost
FROM focus_data_table
WHERE ChargeCategory='Usage'
  AND ChargePeriodStart >= ? AND ChargePeriodEnd <= ?
  AND AllocatedResourceId = ?
GROUP BY
  ResourceId,
  COALESCE(AllocatedResourceId, 'Unallocated')
```

## Example SQL Query (Extract JSON from AllocatedMethodDetails)

```sql
SELECT
  resource_id,
  elements.allocated_ratio,
  elements.usage_unit,
  elements.usage_quantity
FROM
  focus_data_table,
  JSON_TABLE(
    AllocatedMethodDetails,
    '$.Elements[*]' COLUMNS (
      allocated_ratio DECIMAL(10, 2) PATH '$.AllocatedRatio',
      usage_unit VARCHAR(50) PATH '$.UsageUnit',
      usage_quantity DECIMAL(10, 2) PATH '$.UsageQuantity'
    )
  ) AS elements
```

## Introduced (Version)

1.3

---

# Data Granularity

## Description

FOCUS supports multiple levels of cost and usage data granularity. This includes the ability to report on a daily, hourly, or other time period basis. FOCUS also supports the ability for cost and usage data to be provided for high granularity scenarios, such as down to the individual resources. It also supports high level granularity cost and usage data, such as account level, or service level charges.

## Directly Dependent Columns

* ResourceId
* ResourceName
* ChargePeriodEnd
* ChargePeriodStart

## Supporting Columns

* BilledCost
* ConsumedQuantity
* ConsumedUnit
* EffectiveCost
* ListCost
* PricingCurrency
* PricingUnit

## Example SQL Query

```sql
SELECT
  ChargePeriodStart,
  ChargePeriodEnd,
  ResourceId,
  SUM(EffectiveCost)
FROM focus_data_table
Group by
  ChargePeriodStart,
  ChargePeriodEnd,
  ResourceId
```

## Introduced (Version)

0.5

---

# Dataset Instance Metadata

## Description

FOCUS supports the ability for data generators to provide metadata that describes information about the *dataset artifacts* they provide. This includes properties such as the name of the *dataset instance*, the unique identifier of the *dataset instance*, and the *FOCUS dataset* that it aligns with. This metadata can be used by consumers to understand the context of the data they are receiving, and to ensure that they are working with the correct dataset instance to execute their particular FinOps use cases.

## Applicable Metadata

* Dataset Instance
  * Dataset Instance ID
  * Dataset Instance Name
  * FOCUS Dataset ID

## Introduced (Version)

1.3

---

# Effective Cost Analysis

## Description

FOCUS enables practitioners to analyze costs without having to distribute upfront fees and discounts, taking discounts and the amortization of upfront fees paid for services into account. The EffectiveCost column represents cost after negotiated discounts, commitment discounts, and the applicable portion of relevant, prepaid purchases (one-time or recurring) that covered this charge. EffectiveCost is commonly utilized to track and analyze spending trends.

## Directly Dependent Columns

* EffectiveCost

## Supporting Columns

* BillingPeriodEnd
* BillingPeriodStart
* ChargeCategory
* ChargePeriodEnd
* ChargePeriodStart
* ConsumedQuantity
* ConsumedUnit
* PricingQuantity
* ServiceProviderName
* RegionName
* ServiceName

## Example SQL Query

```sql
SELECT
  ServiceProviderName,
  BillingPeriodStart,
  BillingPeriodEnd,
  ServiceCategory,
  ServiceName,
  RegionId,
  RegionName,
  PricingUnit,
  SUM(EffectiveCost) AS TotalEffectiveCost,
  SUM(PricingQuantity) AS TotalPricingQuantity
FROM focus_data_table
WHERE BillingPeriodStart >= ? AND BillingPeriodEnd <= ?
GROUP BY
  ServiceProviderName,
  BillingPeriodStart,
  BillingPeriodEnd,
  ServiceCategory,
  ServiceName,
  RegionId,
  RegionName,
  PricingUnit
```

## Introduced (Version)

0.5

---

# Location

## Description

FOCUS provides structured location data through region and availability zone information. By documenting geographic deployment locations, practitioners can organize and analyze costs based on where resources and services are deployed. This standardized location data helps practitioners understand the geographical distribution of infrastructure across host providers.

## Directly Dependent Columns

* AvailabilityZone
* RegionId
* RegionName

## Supporting Columns

* BilledCost
* ChargePeriodEnd
* ChargePeriodStart

## Example SQL Query

```sql
SELECT
  RegionId,
  RegionName,
  AvailabilityZone,
  SUM(BilledCost) AS TotalBilledCost
FROM focus_data_table
WHERE ChargePeriodStart >= ? AND ChargePeriodEnd <= ?
GROUP BY
  RegionId,
  RegionName,
  AvailabilityZone
```

## Introduced (Version)

1.0

---

# Marketplace Purchases

## Description

FOCUS supports the analysis of cost and usage data for marketplace purchases and their associated costs. It also supports the reporting of EffectiveCost for usage from the service provider.

## Directly Dependent Columns

* InvoiceIssuerName
* ServiceProviderName

## Supporting Columns

* BilledCost
* EffectiveCost

## Example SQL Query on a CSP Marketplace using the Cost and Usage FOCUS Dataset

```sql
SELECT
  ServiceProviderName,
  InvoiceIssuerName,
  BillingPeriodStart,
  BillingPeriodEnd,
  SUM(BilledCost) AS TotalBilledCost
FROM focus_data_table
WHERE ServiceProviderName = '<Example SaaS Provider>'
  AND InvoiceIssuerName = '<Example CSP Marketplace>'
GROUP BY
  ServiceProviderName,
  InvoiceIssuerName,
  BillingPeriodStart,
  BillingPeriodEnd
```

## Example SQL Query on a Provider using the Cost and Usage FOCUS Dataset

```sql
SELECT
  ChargePeriodStart,
  ChargePeriodEnd,
  ResourceId,
  SUM(EffectiveCost) AS TotalEffectiveCost
FROM focus_data_table
WHERE InvoiceIssuerName = '<Example CSP Marketplace>'
GROUP BY
  ChargePeriodStart,
  ChargePeriodEnd,
  ResourceId
```

## Introduced (Version)

1.0

---

# Participating Entity Identification

## Description

FOCUS allows practitioners to identify the several participating entities involved in resource or service hosting, invoicing, and data generation. The FOCUS Specification includes multiple columns to identify key participating entities, including Service Provider Name, Invoice Issuer Name, Host Provider Name, and Data Generator.

## Directly Dependent Columns

* ServiceProviderName
* InvoiceIssuerName
* HostProviderName

## Applicable Metadata

* DataGenerator

## Example SQL Query

```sql
SELECT
  BillingPeriodStart,
  BillingPeriodEnd,
  ServiceProviderName,
  InvoiceIssuerName,
  HostProviderName,
  ServiceName,
  BillingCurrency,
  SUM(BilledCost) AS TotalBilledCost
FROM focus_data_table
WHERE BillingPeriodStart >= ? and BillingPeriodEnd < ?
GROUP BY
  BillingPeriodStart,
  BillingPeriodEnd,
  ServiceProviderName,
  InvoiceIssuerName,
  HostProviderName,
  ServiceName,
  BillingCurrency
```

## Introduced (Version)

1.1

## Updated (Version)

1.3

---

# Recency Metadata

## Description

FOCUS supports the ability for data generators to provide metadata indicating 1) what portion of a FOCUS dataset artifact is complete (either in total, or per time sector), and 2) how recently it has been updated. This metadata allows practitioners to understand whether a given subset of FOCUS data is subject to further change, which informs when and whether they can perform various FinOps functions such as chargeback.

## Applicable Metadata

* Recency
  * Dataset Instance Complete
  * Dataset Instance Last Updated
  * Dataset Instance ID
  * Recency Last Updated
  * Time Sectors
    * Time Sector Start
    * Time Sector End
    * Time Sector Complete
    * Time Sector Last Updated

## Introduced (Version)

1.3

---

# Resource Usage

## Description

FOCUS enables tracking of resource consumption by providing information about which resources were used, in what quantities, and with what units of measure.

## Directly Dependent Columns

* ConsumedQuantity
* ConsumedUnit
* ResourceId
* SkuId

## Supporting Columns

* ChargeCategory
* ChargePeriodEnd
* ChargePeriodStart
* ServiceProviderName
* ServiceName

## Example SQL Query

```sql
SELECT
  ServiceProviderName,
  ServiceName,
  ResourceId,
  SkuId,
  ConsumedUnit,
  SUM(ConsumedQuantity) AS TotalQuantity
FROM focus_data_table
WHERE ChargeCategory='Usage'
  AND ChargePeriodStart >= ? AND ChargePeriodEnd <= ?
GROUP BY
  ServiceProviderName,
  ServiceName,
  ResourceId,
  SkuId,
  ConsumedUnit
```

## Introduced (Version)

1.0

---

# Schema Metadata

## Description

FOCUS' schema metadata supports communication of important attributes about the data, facilitating notifications about changing structure and database table creation between data generator and consumer. This includes column names, data types, and any other relevant information about the data schema. It also includes information as to the version of FOCUS and Data Generator versioning that the data uses.

## Applicable Metadata

* Schema
  * Column Definition

## Introduced (Version)

1.1

---

# Service Categorization

## Description

FOCUS provides a structure for categorizing services based on their core functions. By classifying services into high-level categories and more granular subcategories, practitioners can organize costs according to functional areas. This standardized categorization provides data that practitioners can use in their cost management processes and decision making.

## Directly Dependent Columns

* ServiceCategory
* ServiceName
* ServiceSubcategory

## Supporting Columns

* BilledCost
* BillingCurrency
* BillingPeriodEnd
* BillingPeriodStart
* ServiceProviderName

## Example SQL Query

```sql
SELECT
  BillingPeriodStart,
  BillingPeriodEnd,
  ServiceProviderName,
  ServiceCategory,
  ServiceSubcategory,
  ServiceName,
  BillingCurrency,
  SUM(BilledCost) AS TotalBilledCost
FROM focus_data_table
WHERE BillingPeriodStart >= ? and BillingPeriodEnd < ?
GROUP BY
  BillingPeriodStart,
  BillingPeriodEnd,
  ServiceProviderName,
  ServiceCategory,
  ServiceSubcategory,
  ServiceName,
  BillingCurrency
```

## Introduced (Version)

1.1

---

# Service Provider Services

## Description

FOCUS supports service providers specifying the services and product offerings that they provide their customers that align with the names practitioners are familiar with. This empowers practitioners to analyze cost by service, report service costs by subaccount, forecast based on historical trends by service, and verify accuracy of services charged across service providers.

## Directly Dependent Columns

* ServiceCategory
* ServiceName
* ServiceSubcategory

## Supporting Columns

* ServiceProviderName
* SkuId

## Example SQL Query

```sql
SELECT
  BillingPeriodStart,
  ServiceProviderName,
  SubAccountId,
  SubAccountName,
  ServiceName,
  SUM(BilledCost) AS TotalBilledCost,
  SUM(EffectiveCost) AS TotalEffectiveCost
FROM focus_data_table
WHERE ServiceName = ?
  AND BillingPeriodStart >= ? AND BillingPeriodStart < ?
GROUP BY
  BillingPeriodStart,
  ServiceProviderName,
  SubAccountId,
  SubAccountName,
  ServiceName
ORDER BY MonthlyCost DESC
```

## Introduced (Version)

0.5

---

# Verification, Comparison, and Fluctuation Tracking of Unit Prices

## Description

When a service provider supports unit pricing concepts, FOCUS allows practitioners to:

* Verify that the correct List Unit Prices and Contracted Unit Prices are applied.
* Compare applied Contracted Unit Prices across different billing accounts and with applied List Unit Prices at specific points in time.
* Track fluctuations in unit prices over time.

## Directly Dependent Columns

* ContractedUnitPrice
* ListUnitPrice
* SkuId
* SkuPriceDetails
* SkuPriceId

## Supporting Columns

* BillingCurrency
* BillingPeriodId
* ChargePeriodEnd
* ChargePeriodStart

## Example SQL Query

```sql
SELECT DISTINCT
  SkuId,
  SkuPriceId,
  SkuPriceDetails,
  BillingPeriodId,
  ChargePeriodStart,
  ChargePeriodEnd,
  BillingCurrency,
  ListUnitPrice,
  ContractedUnitPrice
FROM focus_data_table
WHERE
  SkuPriceId = ?
  AND ChargePeriodStart >= ?
  AND ChargePeriodEnd < ?
```

## Introduced (Version)

1.0
