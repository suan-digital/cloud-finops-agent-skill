<!-- Source: FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec (Community Specification License 1.0) -->

# Cost and Usage Columns

# Allocated Method Details

Allocated Method Details provides information about how resources are allocated when usage records are split to support cost allocation requirements.

Allocated Method Details consists of a valid JSON object which contains an array consisting of key-value objects describing the one or more factors that determined the split cost allocation. Each object consists of FOCUS-defined keys but can be extended to provide additional details about the allocation.

The FOCUS-defined properties are:

* `Allocated Ratio`: The ratio of a *charge* that this allocation represents.
* `Usage Unit`: Unit being measured used to calculate this allocation.
* `Usage Quantity`: The quantity of units used denominated by the defined usage unit.

In addition to these, a data generator may include one or more custom properties, also denoted as key-value pairs.

## Requirements

### Column Requirements

The AllocatedMethodDetails column adheres to the following requirements:

* AllocatedMethodDetails SHOULD be present in a Cost and Usage *FOCUS dataset* when the data generator supports Data Generator-Calculated Split Cost Allocation.
* AllocatedMethodDetails MUST be of type String.
* AllocatedMethodDetails MUST conform to StringHandling requirements.
* AllocatedMethodDetails MUST conform to JsonObjectFormat requirements.
* AllocatedMethodDetails nullability is defined as follows:
  * AllocatedMethodDetails MUST be null when a charge is not related to a data generator-calculated split cost allocation.
  * AllocatedMethodDetails SHOULD NOT be null when a charge is related to a data generator-calculated split cost allocation.

### Object Schema Requirements

Allocated Method Details consists of a valid JSON object which contains an array of key-value objects describing the one or more factors (allocation properties) that determined the split cost allocation. Each object consists of FOCUS-defined keys but can be extended to provide additional details about the allocation.

When AllocatedMethodDetails is not null, the JsonObjectFormat for AllocatedMethodDetails adheres to the following requirements:
* AllocatedMethodDetails MUST have a top-level key "Elements" which contains an array.
* Each item in "Elements" MUST be an object.
  * Objects inside "Elements" MUST conform to KeyValueFormat requirements.
    * FOCUS-defined allocation properties adhere to the following additional requirements:
      * Allocation property key MUST match the spelling and casing specified for the FOCUS-defined property.
      * Allocation property value MUST be of the type specified for that property.
      * Allocation properties MUST adhere to additional normative requirements specific to that property.
    * Data generator-defined allocation properties MAY be included in "Elements".
      * Allocation property keys MUST begin with the string "x_" unless it is a FOCUS-defined allocation property.
* AllocatedMethodDetails root object MAY contain additional data generator-defined items, in addition to "Elements".

### Content Requirements

The following keys are used for allocation properties to facilitate querying data across allocations and across data generators. Focus-defined keys will appear in the list below and data generator-defined keys will be prefixed with "x_" to make them easy to identify as well as prevent collisions.

<b>Allocated Ratio</b>

Allocated Ratio communicates the percentage of the *Origin Charge* that this *Allocated Charge* derived from the corresponding Allocated Method Id and Usage Unit property.

The "AllocatedRatio" property adheres to the following requirements:

* "AllocatedRatio" MUST be included inside each "Elements" object.
* Values for "AllocatedRatio" MUST be a decimal value compatible with NumericFormat representing the allocated charge's percentage of the origin charge.
* Values for all "AllocatedRatio" properties across all allocated charges related to a single origin charge MUST sum up to 1 (100%).

<b>Usage Unit</b>

Usage Unit communicates the aspect of the documented Allocation Method Id being used to calculate the Allocated Ratio property and what is being measured by Usage Quantity property.

The "UsageUnit" property adheres to the following requirements:

* "UsageUnit" MUST be included inside an "Elements" object if "UsageQuantity" allocation property is included in that "Elements" object, otherwise "UsageUnit" MAY be included in each "Elements" object.
* Values for "UsageUnit" MUST capture the unit or component of data generator's documented AllocationMethod that was used to determine the "AllocatedRatio" value.
* Values for "UsageUnit" SHOULD conform to UnitFormat requirements.

<b>Usage Quantity</b>

Usage Quantity communicates the volume that was consumed or used, denominated in the Usage Unit property value.

The "UsageQuantity" property adheres to the following requirements:

* "UsageQuantity" MAY be included inside an "Elements" object when that "Elements" object contains a "UsageUnit" allocation property.
* Values for "UsageQuantity" MUST be compatible with NumericFormat.
* Values for "UsageQuantity" SHOULD capture the quantity or volume of the "UsageUnit" measured by the data generator that was used to determine the "AllocatedRatio" value.

## Overview

### Array of Objects

The parent array is called `Elements` and contains one or more objects which communicate information about how an allocated record was calculated.

| Key | ValueType | Required | Description |
| ----- | ---- | ---------- | ----------- |
| Elements | Array | True | The parent array containing one or more objects which communicate information about how an allocated record was calculated. |

### Object Entries

The `Elements` array contains one or more objects, each of which contains the following entries:

| Key | ValueType | Required | Description |
| ----- | ---- | ---------- | ----------- |
| AllocatedRatio | Numeric | True | Percentage of overall cost derived from corresponding method and metric. |
| UsageUnit | String | Conditional | Unit being measured used to calculate allocation. |
| UsageQuantity | Numeric | False | Volume of UsageUnit consumed or used. |

### Example

```json
{
  "Elements" : [ {
    "AllocatedRatio" : 0.05,
    "UsageUnit" : "CPU",
    "UsageQuantity" : 0.5
  }, {
    "AllocatedRatio" : 0.1,
    "UsageUnit" : "Memory",
    "UsageQuantity" : 4
  } ]
}
```

### JSON Type Definition

```json
{
  "properties": {
    "Elements": {
      "elements": {
        "properties": {
          "AllocatedRatio": { "type": "float64" }
        },
        "optionalProperties": {
          "UsageUnit": { "type": "string" },
          "UsageQuantity": { "type": "float64" }
        },
        "additionalProperties": true
      }
    }
  },
  "additionalProperties": true
}
```

NOTE: The above JSON Type Definition (JTD) is an approximation of the expected contents of this column, but it should not be considered normative because it cannot accurately describe the normative requirements (above) for AllocatedMethodDetails. Where there are discrepancies, deference will be given to the normative requirements. For example, NumericFormat allows for multiple numeric data types and precisions, but JTD requires both to be specified; other numeric data types and precisions allowable under NumericFormat are considered valid.

## Example Scenarios

The JSON samples in the scenarios below each represent a single allocated record out of the multiple records derived from an origin record for that scenario. The sum AllocatedRatio will add up to 1 (100%) across all allocated records for an origin record, with the AllocatedRatio (or sum of AllocatedRatio) representing the allocated record's portion of the overall origin record.

### Scenario 1: Single "UsageUnit" value used for allocation

When only a single "UsageUnit" is used to calculate the allocation.

```json
{
  "Elements" : [ {
    "AllocatedRatio" : 0.1,
    "UsageUnit" : "Hours",
    "UsageQuantity" : 300
    }
  ]
}
```
### Scenario 2: Multiple "UsageUnit" values used for allocation

When multiple "UsageUnit" values are used to calculate the allocation, another object is added to the "Elements" collection.

```json
{
  "Elements": [
    {
      "AllocatedRatio": 0.05,
      "UsageUnit": "CPU",
      "UsageQuantity": 0.5
    },
    {
      "AllocatedRatio": 0.1,
      "UsageUnit": "Memory",
      "UsageQuantity": 4
    }
  ]
}
```
### Scenario 3: Data generator omits keys that are not required

This data generator does not wish to supply the "UsageUnit" or "UsageQuantity" keys but still provides cost allocation with some additional allocation method details. In this case, "UsageUnit" and "UsageQuantity" are omitted, and only the "AllocatedRatio" is supplied.

```json
{
  "Elements" : [ {
    "AllocatedRatio" : 0.45
    }
  ]
}
```
### Scenario 4: Additional non-FOCUS specified properties

A data generator can add additional properties if they feel more context is helpful or necessary to the practitioner. In this scenario, the data generator is supplying additional context that shows only 0.5 of a unit was used. However, since 1 unit was requested by the service this allocation represents, the allocation is being charged at 1 regardless.

```json
{
  "Elements": [
    {
      "AllocatedRatio": 0.6,
      "UsageUnit": "vCPU",
      "UsageQuantity": 1,
      "x_ReservedVCPU": 1,
      "x_UsedVCPU": 0.5,
      "x_AllocatedVCPU": 1
    }
  ]
}
```
## Column ID

AllocatedMethodDetails

## Display Name

Allocated Method Details

## Description

A set of properties describing how resources are allocated in data generator-defined split cost allocation.

## Content Constraints

| Constraint      | Value           |
|:----------------|:----------------|
| Column type     | Dimension       |
| Feature level   | Recommended     |
| Allows nulls    | True            |
| Data type       | JSON            |
| Value format    | JSON Object Format |

## Introduced (version)

1.3

---

# Allocated Method ID

Allocated Method ID is the unique identifier for the allocated method defined by the service provider which was used for the Data Generator-Calculated Split Cost Allocation. This unique identifier can be used to find how the allocated charge was calculated in the provider's documentation.

## Requirements

AllocatedMethodId adheres to the following requirements:

* AllocatedMethodId MUST be present in a Cost and Usage *FOCUS dataset* when the data generator supports data generator-calculated split cost allocation.
* AllocatedMethodId MUST be of type String.
* AllocatedMethodId MUST conform to StringHandling requirements.
* AllocatedMethodId nullability is defined as follows:
  * AllocatedMethodId MUST be null when a *charge* is not related to a data generator-calculated split cost allocation.
  * AllocatedMethodId MUST NOT be null when a *charge* is related to a data generator-calculated split cost allocation.
* Data generator documentation of a split cost allocation method MUST make reference to a single AllocatedMethodId value.

## Column ID

AllocatedMethodId

## Display Name

Allocated Method ID

## Description

A unique identifier defining the method of data generator-calculated split cost allocation.

## Content constraints

|    Constraint   |      Value       |
|:----------------|:-----------------|
| Column type     | Dimension        |
| Feature level   | Conditional      |
| Allows nulls    | True             |
| Data type       | String           |
| Value format    | \<not specified> |

## Introduced (version)

1.3

---

# Allocated Resource ID

An Allocated Resource ID is an identifier assigned by the data generator which cost is being allocated to in a Data Generator-Calculated Split Cost Allocation. The Allocated Resource ID is used to understand what the cost is being allocated to in *charges* where the data generator is allocating costs to something other than the *charge's* ResourceID, as is the case for allocated charges.

## Requirements

AllocatedResourceId adheres to the following requirements:

* AllocatedResourceId MUST be present in a Cost and Usage *FOCUS dataset* when the service provider supports data generator-calculated split cost allocation.
* AllocatedResourceId MUST be of type String.
* AllocatedResourceId MUST conform to StringHandling requirements.
* AllocatedResourceId nullability is defined as follows:
  * AllocatedResourceId MUST be null when a *charge* is not related to a data generator-calculated split cost allocation.
  * AllocatedResourceId MUST be null when a *charge* represents the unallocated portion of the origin *charge* after split cost allocation.
  * AllocatedResourceId MUST NOT be null when a *charge* represents the allocated portion of the origin *charge*.
* When AllocatedResourceId is not null, AllocatedResourceId adheres to the following additional requirements:
  * AllocatedResourceId SHOULD be a locally unique identifier within the associated ResourceId and ChargePeriod.
  * AllocatedResourceId MAY NOT be unique across ResourceId or ChargePeriod values.

## Column ID

AllocatedResourceId

## Display Name

Allocated Resource ID

## Description

The identifier of the object to which cost is allocated in data generator-calculated split cost allocation.

## Content Constraints

| Constraint      | Value           |
|:----------------|:----------------|
| Column type     | Dimension       |
| Feature level   | Conditional     |
| Allows nulls    | True            |
| Data type       | String          |
| Value format    | \<not specified> |

## Introduced (version)

1.3

---

# Allocated Resource Name

The Allocated Resource Name is a display name which cost is being allocated to in a Data Generator-Calculated Split Cost Allocation. The Allocated Resource Name is used to understand what the cost is being allocated to in *charges* where the service provider is allocating costs to something other than the charge's ResourceID, as is the case for allocated charges.

## Requirements

AllocatedResourceName adheres to the following requirements:

* AllocatedResourceName MUST be present in a Cost and Usage *FOCUS dataset* when the service provider supports data generator-calculated split cost allocation.
* AllocatedResourceName MUST be of type String.
* AllocatedResourceName MUST conform to StringHandling requirements.
* AllocatedResourceName nullability is defined as follows:
  * AllocatedResourceName MUST be null when AllocatedResourceId is null.
  * AllocatedResourceName MUST NOT be null when AllocatedResourceId is not null.
* AllocatedResourceName MAY duplicate AllocatedResourceId when a separate display name is not applicable.

## Column ID

AllocatedResourceName

## Display Name

Allocated Resource Name

## Description

The display name of the object to which cost is allocated in data generator-calculated split cost allocation.

## Content Constraints

| Constraint      | Value           |
|:----------------|:----------------|
| Column type     | Dimension       |
| Feature level   | Conditional     |
| Allows nulls    | True            |
| Data type       | String          |
| Value format    | \<not specified> |

## Introduced (version)

1.3

---

# Allocated Tags

The Allocated Tags column represents the set of *tags* assigned to *tag sources* which are specifically applicable to *allocated charges* resulting from a data generator-calculated split cost allocation.

## Requirements

AllocatedTags adheres to the following requirements:

* AllocatedTags MUST be present in a Cost and Usage *FOCUS dataset* when the service provider supports Data Generator-Calculated Split Cost Allocation.
* AllocatedTags MUST conform to KeyValueFormat requirements.
* AllocatedTags nullability is defined as follows:
  * AllocatedTags MUST be null when a *charge* is not related to a data generator-calculated split cost allocation.
  * AllocatedTags MAY be null in all other cases.
* When AllocatedTags is not null, AllocatedTags adheres to the following additional requirements:
  * AllocatedTags MUST NOT include resource tags already present in Tags.
  * AllocatedTags MUST include all applicable user-defined and data generator-defined tags for the AllocatedResourceId.
  * Tag keys that do not support corresponding values MUST have a corresponding true (boolean) value set.
  * Data generator MUST NOT alter tag values unless applying true (boolean) to valueless tags.
* Data generator-defined tags adhere to the following additional requirements:
  * Data generator-defined tag keys MUST be prefixed with a predetermined, data generator-specified tag key prefix that is unique to each corresponding provider-specified tag scheme.
  * Data generator SHOULD publish all data generator-specified tag key prefixes within their respective documentation.
* User-defined tags adhere to the following additional requirements:
  * Data generator MUST prefix all user-defined tags scheme with a predetermined, data generator-specified tag key prefix that is unique to each corresponding user-defined tag scheme when the data generator has more than one user-defined tag scheme.

## Data Generator-Defined vs. User-Defined Tags

This example illustrates various tags produced from multiple user-defined and data generator-defined tag schemes. The first two tags illustrate examples from two different, user-defined tag schemes. The second tag is produced from a valueless, user-defined tag scheme, so the data generator also applies `true` as its default value.

The last two tags illustrate examples from two different, data generator-defined tag schemes.

```json
    {
        "userDefinedTagScheme1/foo": "bar",
        "userDefinedTagScheme2/foo": true,
        "providerDefinedTagScheme1/foo": "bar",
        "providerDefinedTagScheme2/foo": "bar"
    }
```

## Column ID

AllocatedTags

## Display Name

Allocated Tags

## Description

A set of tags assigned to tag sources that are applicable to *allocated charges* in data generator-calculated split cost allocation.

## Content Constraints

|    Constraint   |      Value       |
|:----------------|:-----------------|
| Column type     | Dimension        |
| Feature level   | Conditional      |
| Allows nulls    | True             |
| Data type       | JSON             |
| Value format    | Key-Value Format |

## Introduced (version)

1.3

---

# Availability Zone

An *availability zone* is a host-provider-assigned identifier for a physically separated and isolated area within a Region that provides high availability and fault tolerance. Availability Zone is commonly used for scenarios like analyzing cross-zone data transfer usage and the corresponding cost based on where *resources* are deployed.

## Requirements

AvailabilityZone adheres to the following requirements:

* AvailabilityZone is RECOMMENDED to be present in a Cost and Usage *FOCUS dataset* when the host provider supports deploying resources or services within an *availability zone*.
* AvailabilityZone MUST be of type String.
* AvailabilityZone MUST conform to StringHandling requirements.
* AvailabilityZone MUST be null when a *charge* is not specific to an *availability zone*.

## Column ID

AvailabilityZone

## Display Name

Availability Zone

## Description

A host-provider-assigned identifier for a physically separated and isolated area within a Region that provides high availability and fault tolerance.

## Content constraints

| Constraint      | Value            |
|:----------------|:-----------------|
| Column type     | Dimension        |
| Feature level   | Recommended      |
| Allows nulls    | True             |
| Data type       | String           |
| Value format    | \<not specified> |

## Introduced (version)

0.5

---

# Billed Cost

The *billed cost* represents a *charge* serving as the basis for invoicing, inclusive of the impacts of all reduced rates and discounts while excluding the *amortization* of relevant purchases (one-time or recurring) paid to cover future eligible *charges*. This cost is denominated in the Billing Currency. The Billed Cost is commonly used to perform FinOps capabilities that require cash-basis accounting such as cost allocation, budgeting, and invoice reconciliation.

## Requirements

BilledCost adheres to the following requirements:

* BilledCost MUST be present in a Cost and Usage *FOCUS dataset*.
* BilledCost MUST be of type Decimal.
* BilledCost MUST conform to NumericFormat requirements.
* BilledCost MUST NOT be null.
* BilledCost MUST be a valid decimal value.
* BilledCost MUST be 0 for *charges* where payments are received by a third party (e.g., marketplace transactions).
* BilledCost MUST be denominated in the BillingCurrency.
* The sum of the BilledCost for a given InvoiceId MUST match the sum of the payable amount provided in the corresponding invoice with the same id generated by the InvoiceIssuerName.

## Column ID

BilledCost

## Display Name

Billed Cost

## Description

A *charge* serving as the basis for invoicing, inclusive of all reduced rates and discounts while excluding the *amortization* of upfront *charges* (one-time or recurring).

## Content constraints

|    Constraint   |      Value              |
|:----------------|:------------------------|
| Column type     | Metric                  |
| Feature level   | Mandatory               |
| Allows nulls    | False                   |
| Data type       | Decimal                 |
| Value format    | Numeric Format |
| Number range    | Any valid decimal value |

## Introduced (version)

0.5

---

# Billing Account ID

A Billing Account ID is an invoice-issuer-assigned identifier for a *billing account*. *Billing accounts* are commonly used for scenarios like grouping based on organizational constructs, invoice reconciliation and cost allocation strategies.

## Requirements

BillingAccountId adheres to the following requirements:

* BillingAccountId MUST be present in a Cost and Usage *FOCUS dataset*.
* BillingAccountId MUST be of type String.
* BillingAccountId MUST conform to StringHandling requirements.
* BillingAccountId MUST NOT be null.
* BillingAccountId MUST be a unique identifier within an invoice issuer.
* BillingAccountId SHOULD be a fully-qualified identifier.

See Appendix: Grouping constructs for resources or services for details and examples of the different grouping constructs supported by FOCUS.

## Column ID

BillingAccountId

## Display Name

Billing Account ID

## Description

The identifier assigned to a *billing account* by the invoice issuer.

## Content constraints

|    Constraint   |      Value       |
|:----------------|:-----------------|
| Column type     | Dimension        |
| Feature level   | Mandatory        |
| Allows nulls    | False            |
| Data type       | String           |
| Value format    | \<not specified> |

## Introduced (version)

0.5

---

# Billing Account Name

A Billing Account Name is a display name assigned to a *billing account*. *Billing accounts* are commonly used for scenarios like grouping based on organizational constructs, invoice reconciliation and cost allocation strategies.

## Requirements

BillingAccountName adheres to the following requirements:

* BillingAccountName MUST be present in a Cost and Usage *FOCUS dataset*.
* BillingAccountName MUST be of type String.
* BillingAccountName MUST conform to StringHandling requirements.
* BillingAccountName MUST NOT be null when the invoice issuer supports assigning a display name for the *billing account*.

See Appendix: Grouping constructs for resources or services for details and examples of the different grouping constructs supported by FOCUS.

## Column ID

BillingAccountName

## Display Name

Billing Account Name

## Description

The display name assigned to a *billing account*.

## Content constraints

|    Constraint   |      Value       |
|:----------------|:-----------------|
| Column type     | Dimension        |
| Feature level   | Mandatory        |
| Allows nulls    | True             |
| Data type       | String           |
| Value format    | \<not specified> |

## Introduced (version)

0.5

---

# Billing Account Type

Billing Account Type is an invoice-issuer-assigned name to identify the type of *billing account*. Billing Account Type is a readable display name and not a code. Billing Account Type is commonly used for scenarios like mapping FOCUS and provider constructs, summarizing costs across providers, or invoicing and chargeback.

## Requirements

BillingAccountType adheres to the following requirements:

* BillingAccountType MUST be present in a Cost and Usage *FOCUS dataset* when the invoice issuer supports more than one possible BillingAccountType value.
* BillingAccountType MUST be of type String.
* BillingAccountType MUST conform to StringHandling requirements.
* BillingAccountType nullability is defined as follows:
  * BillingAccountType MUST be null when BillingAccountId is null.
  * BillingAccountType MUST NOT be null when BillingAccountId is not null.
* BillingAccountType MUST be a consistent, readable display value.

## Column ID

BillingAccountType

## Display Name

Billing Account Type

## Description

An invoice-issuer-assigned name to identify the type of *billing account*.

## Content Constraints

| Constraint      | Value            |
| :-------------- | :--------------- |
| Column type     | Dimension        |
| Feature level   | Conditional      |
| Allows nulls    | False            |
| Data type       | String           |
| Value format    | \<not specified> |

## Introduced (version)

1.2

---

# Billing Currency

*Billing currency* is an identifier that represents the currency that a *charge* for *resources* or *services* was billed in. Billing Currency is commonly used in scenarios where costs need to be grouped or aggregated.

## Requirements

BillingCurrency adheres to the following requirements:

* BillingCurrency MUST be present in a Cost and Usage *FOCUS dataset*.
* BillingCurrency MUST be of type String.
* BillingCurrency MUST conform to StringHandling requirements.
* BillingCurrency MUST conform to CurrencyFormat requirements.
* BillingCurrency MUST NOT be null.
* BillingCurrency MUST match the currency used in the invoice generated by the invoice issuer.
* BillingCurrency MUST be expressed in *national currency* (e.g., USD, EUR).

## Column ID

BillingCurrency

## Display Name

Billing Currency

## Description

Represents the currency that a *charge* was billed in.

## Content Constraints

| Constraint      | Value                               |
|:----------------|:------------------------------------|
| Column type     | Dimension                           |
| Feature level   | Mandatory                           |
| Allows nulls    | False                               |
| Data type       | String                              |
| Value format    | Currency Format |

## Introduced (version)

0.5

---

# Billing Period End

Billing Period End represents the *exclusive end bound* of a *billing period*. For example, a time period where Billing Period Start is '2024-01-01T00:00:00Z' and Billing Period End is '2024-02-01T00:00:00Z' includes *charges* for January since Billing Period Start represents the *inclusive start bound*, but does not include *charges* for February since Billing Period End represents the *exclusive end bound*.

## Requirements

BillingPeriodEnd adheres to the following requirements:

* BillingPeriodEnd MUST be present in a Cost and Usage *FOCUS dataset*.
* BillingPeriodEnd MUST be of type Date/Time.
* BillingPeriodEnd MUST conform to DateTimeFormat requirements.
* BillingPeriodEnd MUST NOT be null.
* BillingPeriodEnd MUST be the *exclusive end bound* of the *billing period*.

## Column ID

BillingPeriodEnd

## Display Name

Billing Period End

## Description

The *exclusive end bound* of a *billing period*.

## Content Constraints

| Constraint      | Value                                |
|:----------------|:-------------------------------------|
| Column type     | Dimension                            |
| Feature level   | Mandatory                            |
| Allows nulls    | False                                |
| Data type       | Date/Time                            |
| Value format    | Date/Time Format |

## Introduced (version)

0.5

---

# Billing Period Start

Billing Period Start represents the *inclusive start bound* of a *billing period*. For example, a time period where Billing Period Start is '2024-01-01T00:00:00Z' and Billing Period End is '2024-02-01T00:00:00Z' includes *charges* for January since Billing Period Start represents the *inclusive start bound*, but does not include *charges* for February since BillingPeriodEnd represents the *exclusive end bound*.

## Requirements

BillingPeriodStart adheres to the following requirements:

* BillingPeriodStart MUST be present in a Cost and Usage *FOCUS dataset*.
* BillingPeriodStart MUST be of type Date/Time.
* BillingPeriodStart MUST conform to DateTimeFormat requirements.
* BillingPeriodStart MUST NOT be null.
* BillingPeriodStart MUST be the *inclusive start bound* of the *billing period*.

## Column ID

BillingPeriodStart

## Display Name

Billing Period Start

## Description

The *inclusive start bound* of a *billing period*.

## Content Constraints

| Constraint      | Value                                |
|:----------------|:-------------------------------------|
| Column type     | Dimension                            |
| Feature level   | Mandatory                            |
| Allows nulls    | False                                |
| Data type       | Date/Time                            |
| Value format    | Date/Time Format |

## Introduced (version)

0.5

---

# Capacity Reservation ID

A Capacity Reservation ID is the identifier assigned to a *capacity reservation* by the service provider. Capacity Reservation ID is commonly used for scenarios to allocate *charges* for capacity reservation usage.

## Requirements

CapacityReservationId adheres to the following requirements:

* CapacityReservationId MUST be present in a Cost and Usage *FOCUS dataset* when the service provider supports *capacity reservations*.
* CapacityReservationId MUST be of type String.
* CapacityReservationId MUST conform to StringHandling requirements.
* CapacityReservationId nullability is defined as follows:
  * CapacityReservationId MUST be null when a *charge* is not related to a *capacity reservation*.
  * CapacityReservationId MUST NOT be null when a *charge* represents the unused portion of a *capacity reservation*.
  * CapacityReservationId SHOULD NOT be null when a *charge* is related to a capacity reservation.
* When CapacityReservationId is not null, CapacityReservationId adheres to the following additional requirements:
  * CapacityReservationId MUST be a unique identifier within the service provider.
  * CapacityReservationId SHOULD be a fully-qualified identifier.

## Column ID

CapacityReservationId

## Display Name

Capacity Reservation ID

## Description

The identifier assigned to a *capacity reservation* by the service provider.

## Content constraints

|    Constraint   |      Value       |
|:----------------|:-----------------|
| Column type     | Dimension        |
| Feature level   | Conditional      |
| Allows nulls    | True             |
| Data type       | String           |
| Value format    | \<not specified> |

## Introduced (version)

1.1

---

# Capacity Reservation Status

Capacity Reservation Status indicates whether the *charge* represents either the consumption of the *capacity reservation* identified in the CapacityReservationId column or when the *capacity reservation* is unused.

## Requirements

CapacityReservationStatus adheres to the following requirements:

* CapacityReservationStatus MUST be present in a Cost and Usage *FOCUS dataset* when the service provider supports *capacity reservations*.
* CapacityReservationStatus MUST be of type String.
* CapacityReservationStatus nullability is defined as follows:
  * CapacityReservationStatus MUST be null when CapacityReservationId is null.
  * CapacityReservationStatus MUST NOT be null when CapacityReservationId is not null and ChargeCategory is "Usage".
* When CapacityReservationStatus is not null, CapacityReservationStatus adheres to the following additional requirements:
  * CapacityReservationStatus MUST be one of the allowed values.
  * CapacityReservationStatus MUST be "Unused" when the *charge* represents the unused portion of a *capacity reservation*.
  * CapacityReservationStatus MUST be "Used" when the *charge* represents the used portion of a *capacity reservation*.

## Column ID

CapacityReservationStatus

## Display Name

Capacity Reservation Status

## Description

Indicates whether the *charge* represents either the consumption of a *capacity reservation* or when a *capacity reservation* is unused.

## Content constraints

| Constraint      | Value          |
| :-------------- | :------------- |
| Column type     | Dimension      |
| Feature level   | Conditional    |
| Allows nulls    | True           |
| Data type       | String         |
| Value format    | Allowed Values |

Allowed values:

| Value  | Description                                                                 |
| :----- | :-------------------------------------------------------------------------- |
| Used   | *Charges* that utilized a specific amount of a *capacity reservation*.      |
| Unused | *Charges* that represent the unused portion of a *capacity reservation*.    |

## Introduced (version)

1.1

---

# Charge Category

Charge Category represents the highest-level classification of a *charge* based on the nature of how it is billed. Charge Category is commonly used to identify and distinguish between types of *charges* that may require different handling.

## Requirements

ChargeCategory adheres to the following requirements:

* ChargeCategory MUST be present in a Cost and Usage *FOCUS dataset*.
* ChargeCategory MUST be of type String.
* ChargeCategory MUST NOT be null.
* ChargeCategory MUST be one of the allowed values.

## Column ID

ChargeCategory

## Display Name

Charge Category

## Description

Represents the highest-level classification of a *charge* based on the nature of how it is billed.

## Content Constraints

| Constraint      | Value          |
| :-------------- | :------------- |
| Column type     | Dimension      |
| Feature level   | Mandatory      |
| Allows nulls    | False          |
| Data type       | String         |
| Value format    | Allowed values |

Allowed values:

| Value      | Description                                                                                                                                    |
| :--------- | :----------------------------------------------------------------------------------------------------------------------------------------------|
| Usage      | Positive or negative *charges* based on the quantity of a service or resource that was consumed over a given period of time including refunds. |
| Purchase   | Positive or negative *charges* for the acquisition of a service or resource bought upfront or on a recurring basis including refunds.          |
| Tax        | Positive or negative applicable taxes that are levied by the relevant authorities including refunds. Tax *charges* may vary depending on factors such as the location, jurisdiction, and local or federal regulations. |
| Credit     | Positive or negative *charges* granted by the service provider for various scenarios e.g promotional credits or corrections to promotional credits.    |
| Adjustment | Positive or negative *charges* the service provider applies that do not fall into other category values.                                               |

## Introduced (version)

0.5

---

# Charge Class

Charge Class indicates whether the *row* represents a correction to a previously invoiced *billing period*. Charge Class is commonly used to differentiate *corrections* from regularly incurred *charges*.

## Requirements

ChargeClass adheres to the following requirements:

* ChargeClass MUST be present in a Cost and Usage *FOCUS dataset*.
* ChargeClass MUST be of type String.
* ChargeClass nullability is defined as follows:
  * ChargeClass MUST be null when the *row* does not represent a correction or when it represents a correction within the current *billing period*.
  * ChargeClass MUST NOT be null when the *row* represents a correction to a previously invoiced *billing period*.
* ChargeClass MUST be "Correction" when ChargeClass is not null.

## Column ID

ChargeClass

## Display Name

Charge Class

## Description

Indicates whether the *row* represents a correction to a previously invoiced *billing period*.

## Content Constraints

| Constraint      | Value          |
| :-------------- | :------------- |
| Column type     | Dimension      |
| Feature level   | Mandatory      |
| Allows nulls    | True           |
| Data type       | String         |
| Value format    | Allowed values |

Allowed values:

| Value      | Description                                                                                    |
| :--------- | :----------------------------------------------------------------------------------------------|
| Correction | Correction to a previously invoiced *billing period* (e.g., refunds and credit modifications). |

## Introduced (version)

1.0

---

# Charge Description

A Charge Description provides a high-level context of a *row* without requiring additional discovery. This column is a self-contained summary of the *charge's* purpose and price. It typically covers a select group of corresponding details across a billing dataset or provides information not otherwise available.

## Requirements

ChargeDescription adheres to the following requirements:

* ChargeDescription MUST be present in a Cost and Usage *FOCUS dataset*.
* ChargeDescription MUST be of type String.
* ChargeDescription MUST conform to StringHandling requirements.
* ChargeDescription SHOULD NOT be null.
* ChargeDescription maximum length SHOULD be provided in the corresponding FOCUS Metadata Schema.

## Column ID

ChargeDescription

## Display Name

Charge Description

## Description

Self-contained summary of the *charge's* purpose and price.

## Content Constraints

|    Constraint   |      Value       |
|:----------------|:-----------------|
| Column type     | Dimension        |
| Feature level   | Mandatory        |
| Allows nulls    | True             |
| Data type       | String           |
| Value format    | \<not specified> |

## Introduced (version)

1.0-preview

---

# Charge Frequency

Charge Frequency indicates how often a *charge* will occur. Along with the charge period related columns, the Charge Frequency is commonly used to understand recurrence periods (e.g., monthly, yearly), forecast upcoming *charges*, and differentiate between one-time and recurring fees for purchases.

## Requirements

ChargeFrequency adheres to the following requirements:

* ChargeFrequency is RECOMMENDED to be present in a Cost and Usage *FOCUS dataset*.
* ChargeFrequency MUST be of type String.
* ChargeFrequency MUST NOT be null.
* ChargeFrequency MUST be one of the allowed values.
* ChargeFrequency MUST NOT be "Usage-Based" when ChargeCategory is "Purchase".

## Column ID

ChargeFrequency

## Display Name

Charge Frequency

## Description

Indicates how often a *charge* will occur.

## Content Constraints

| Constraint      | Value          |
|:----------------|:---------------|
| Column type     | Dimension      |
| Feature level   | Recommended    |
| Allows nulls    | False          |
| Data type       | String         |
| Value format    | Allowed values |

Allowed values:

| Value       | Description                   |
|:------------|:------------------------------|
| One-Time    | *Charges* that only happen once and will not repeat. One-time *charges* are typically recorded on the hour or day when the cost was incurred.  |
| Recurring   | *Charges* that repeat on a periodic cadence (e.g., weekly, monthly) regardless of whether the product or *service* was used. Recurring *charges* typically happen on the same day or point within every period. The charge date does not change based on how or when the *service* is used. |
| Usage-Based | *Charges* that repeat every time the *service* is used. Usage-based *charges* are typically recorded hourly or daily, based on the granularity of the cost data for the period when the *service* was used (referred to as *charge period*). Usage-based *charges* are not recorded when the *service* is not used.                    |

## Introduced (version)

1.0-preview

---

# Charge Period End

Charge Period End represents the *exclusive end bound* of a *charge period*. For example, a time period where Charge Period Start is '2024-01-01T00:00:00Z' and Charge Period End is '2024-01-02T00:00:00Z' includes *charges* for January 1 since Charge Period Start represents the *inclusive start bound*, but does not include *charges* for January 2 since Charge Period End represents the *exclusive end bound*.

## Requirements

ChargePeriodEnd adheres to the following requirements:

* ChargePeriodEnd MUST be present in a Cost and Usage *FOCUS dataset*.
* ChargePeriodEnd MUST be of type Date/Time.
* ChargePeriodEnd MUST conform to DateTimeFormat requirements.
* ChargePeriodEnd MUST NOT be null.
* ChargePeriodEnd MUST be the *exclusive end bound* of the effective period of the *charge*.

## Column ID

ChargePeriodEnd

## Display Name

Charge Period End

## Description

The *exclusive end bound* of a *charge period*.

## Content constraints

| Constraint      | Value                                |
|:----------------|:-------------------------------------|
| Column type     | Dimension                            |
| Feature level   | Mandatory                            |
| Allows nulls    | False                                |
| Data type       | Date/Time                            |
| Value format    | Date/Time Format |

## Introduced (version)

0.5

---

# Charge Period Start

Charge Period Start represents the *inclusive start bound* of a *charge period*. For example, a time period where Charge Period Start is '2024-01-01T00:00:00Z' and Charge Period End is '2024-01-02T00:00:00Z' includes *charges* for January 1 since Charge Period Start represents the *inclusive start bound*, but does not include *charges* for January 2 since Charge Period End represents the *exclusive end bound*.

## Requirements

ChargePeriodStart adheres to the following requirements:

* ChargePeriodStart MUST be present in a Cost and Usage *FOCUS dataset*.
* ChargePeriodStart MUST be of type Date/Time.
* ChargePeriodStart MUST conform to DateTimeFormat requirements.
* ChargePeriodStart MUST NOT be null.
* ChargePeriodStart MUST be the *inclusive start bound* of the effective period of the *charge*.

## Column ID

ChargePeriodStart

## Display Name

Charge Period Start

## Description

The *inclusive start bound* of a *charge period*.

## Content constraints

| Constraint      | Value                                |
|:----------------|:-------------------------------------|
| Column type     | Dimension                            |
| Feature level   | Mandatory                            |
| Allows nulls    | False                                |
| Data type       | Date/Time                            |
| Value format    | Date/Time Format |

## Introduced (version)

0.5

---

# Commitment Discount Category

Commitment Discount Category indicates whether the *commitment discount* identified in the CommitmentDiscountId column is based on usage quantity or cost (aka "spend"). The CommitmentDiscountCategory column is only applicable to *commitment discounts* and not *negotiated discounts*.

## Requirements

CommitmentDiscountCategory adheres to the following requirements:

* CommitmentDiscountCategory MUST be present in a Cost and Usage *FOCUS dataset* when the service provider supports *commitment discounts*.
* CommitmentDiscountCategory MUST be of type String.
* CommitmentDiscountCategory nullability is defined as follows:
  * CommitmentDiscountCategory MUST be null when CommitmentDiscountId is null.
  * CommitmentDiscountCategory MUST NOT be null when CommitmentDiscountId is not null.
* CommitmentDiscountCategory MUST be one of the allowed values.

## Column ID

CommitmentDiscountCategory

## Display Name

Commitment Discount Category

## Description

Indicates whether the *commitment discount* identified in the CommitmentDiscountId column is based on usage quantity or cost (aka "spend").

## Content constraints

|    Constraint   |      Value       |
|:----------------|:-----------------|
| Column type     | Dimension        |
| Feature level   | Conditional      |
| Allows nulls    | True             |
| Data type       | String           |
| Value format    | Allowed Values   |

Allowed values:

| Value   | Description                                                              |
|:--------|:-------------------------------------------------------------------------|
| Spend   | Commitment discounts that require a predetermined amount of spend. |
| Usage   | Commitment discounts that require a predetermined amount of usage. |

## Introduced (version)

1.0-preview

---

# Commitment Discount ID

A Commitment Discount ID is the identifier assigned to a *commitment discount* by the service provider. Commitment Discount ID is commonly used for scenarios like chargeback for *commitments* and savings per *commitment discount*. The CommitmentDiscountId column is only applicable to *commitment discounts* and not *negotiated discounts*.

## Requirements

CommitmentDiscountId adheres to the following requirements:

* CommitmentDiscountId MUST be present in a Cost and Usage *FOCUS dataset* when the service provider supports *commitment discounts*.
* CommitmentDiscountId MUST be of type String.
* CommitmentDiscountId MUST conform to StringHandling requirements.
* CommitmentDiscountId nullability is defined as follows:
  * CommitmentDiscountId MUST be null when a *charge* is not related to a *commitment discount*.
  * CommitmentDiscountId MUST NOT be null when a *charge* is related to a *commitment discount*.
* When CommitmentDiscountId is not null, CommitmentDiscountId adheres to the following additional requirements:
  * CommitmentDiscountId MUST be a unique identifier within the service provider.
  * CommitmentDiscountId SHOULD be a fully-qualified identifier.

## Column ID

CommitmentDiscountId

## Display Name

Commitment Discount ID

## Description

The identifier assigned to a *commitment discount* by the service provider.

## Content constraints

|    Constraint   |      Value       |
|:----------------|:-----------------|
| Column type     | Dimension        |
| Feature level   | Conditional      |
| Allows nulls    | True             |
| Data type       | String           |
| Value format    | \<not specified> |

## Introduced (version)

1.0-preview

---

# Commitment Discount Name

A Commitment Discount Name is the display name assigned to a *commitment discount*. The CommitmentDiscountName column is only applicable to *commitment discounts* and not *negotiated discounts*.

## Requirements

CommitmentDiscountName adheres to the following requirements:

* CommitmentDiscountName MUST be present in a Cost and Usage *FOCUS dataset* when the service provider supports *commitment discounts*.
* CommitmentDiscountName MUST be of type String.
* CommitmentDiscountName MUST conform to StringHandling requirements.
* CommitmentDiscountName nullability is defined as follows:
  * CommitmentDiscountName MUST be null when CommitmentDiscountId is null.
  * When CommitmentDiscountId is not null, CommitmentDiscountName adheres to the following additional requirements:
    * CommitmentDiscountName MUST NOT be null when a display name can be assigned to a *commitment discount*.
    * CommitmentDiscountName MAY be null when a display name cannot be assigned to a *commitment discount*.

## Column ID

CommitmentDiscountName

## Display Name

Commitment Discount Name

## Description

The display name assigned to a *commitment discount*.

## Content constraints

| Constraint      | Value            |
|:----------------|:-----------------|
| Column type     | Dimension        |
| Feature level   | Conditional      |
| Allows nulls    | True             |
| Data type       | String           |
| Value format    | \<not specified> |

## Introduced (version)

1.0-preview

---

# Commitment Discount Quantity

Commitment Discount Quantity is the amount of a *commitment discount* purchased or accounted for in *commitment discount* related *rows* that is denominated in Commitment Discount Units. The aggregated Commitment Discount Quantity across purchase records, pertaining to a particular Commitment Discount ID during its commitment *period*, represents the total Commitment Discount Units acquired with that commitment discount. For committed usage, the Commitment Discount Quantity is either the number of Commitment Discount Units consumed by a *row* that is covered by a *commitment discount* or is the unused portion of a *commitment discount* over a *charge period*. Commitment Discount Quantity is commonly used in *commitment discount* analysis and optimization use cases and only applies to *commitment discounts*, not *negotiated discounts*.

When CommitmentDiscountCategory is "Usage" (usage-based *commitment discounts*), the Commitment Discount Quantity reflects the predefined amount of usage purchased or consumed. If *commitment discount flexibility* is applicable, this value may be further transformed based on additional, service-provider-specific requirements. When CommitmentDiscountCategory is "Spend" (spend-based *commitment discounts*), the Commitment Discount Quantity reflects the predefined amount of spend purchased or consumed.  See Appendix: Commitment Discount Flexibility for more details around *commitment discount flexibility*.

## Requirements

CommitmentDiscountQuantity adheres to the following requirements:

* CommitmentDiscountQuantity MUST be present in a Cost and Usage *FOCUS dataset* when the service provider supports *commitment discounts*.
* CommitmentDiscountQuantity MUST be of type Decimal.
* CommitmentDiscountQuantity MUST conform to NumericFormat requirements.
* CommitmentDiscountQuantity nullability is defined as follows:
  * CommitmentDiscountQuantity MUST be null when SkuPriceId is null.
  * When ChargeCategory is "Usage" or "Purchase" and CommitmentDiscountId is not null, CommitmentDiscountQuantity adheres to the following additional requirements:
    * CommitmentDiscountQuantity MUST NOT be null when ChargeClass is not "Correction".
    * CommitmentDiscountQuantity MAY be null when ChargeClass is "Correction".
  * CommitmentDiscountQuantity MUST be null in all other cases.
* CommitmentDiscountQuantity MUST be a valid decimal value when not null.
* When CommitmentDiscountQuantity is not null and ChargeCategory is "Purchase", CommitmentDiscountQuantity adheres to the following additional requirements:
  * CommitmentDiscountQuantity MUST be the quantity of CommitmentDiscountUnit, paid fully or partially upfront, that is eligible for consumption over the *commitment discount's* *term* when ChargeFrequency is "One-Time".
  * CommitmentDiscountQuantity MUST be the quantity of CommitmentDiscountUnit that is eligible for consumption for each *charge period* that corresponds with the purchase when ChargeFrequency is "Recurring".
* When CommitmentDiscountQuantity is not null and ChargeCategory is "Usage", CommitmentDiscountQuantity adheres to the following additional requirements:
  * CommitmentDiscountQuantity MUST be the metered quantity of CommitmentDiscountUnit that is consumed in a given *charge period* when CommitmentDiscountStatus is "Used".
  * CommitmentDiscountQuantity MUST be the remaining, unused quantity of CommitmentDiscountUnit in a given *charge period* when CommitmentDiscountStatus is "Unused".

## Column ID

CommitmentDiscountQuantity

## Display Name

Commitment Discount Quantity

## Description

The amount of a *commitment discount* purchased or accounted for in *commitment discount* related *rows* that is denominated in Commitment Discount Units.

## Usability Constraints

**Aggregation:** When aggregating Commitment Discount Quantity for commitment utilization calculations, it's important to exclude *commitment discount* purchases (i.e. when Charge Category is "Purchase") that are paid to cover future eligible *charges* (e.g., *commitment discount*). Otherwise, when accounting for all upfront or accrued purchases, it's important to exclude *commitment discount* usage (i.e. when Charge Category is "Usage"). This exclusion helps prevent double counting of these quantities in the aggregation.

## Content constraints

| Constraint      | Value            |
|:----------------|:-----------------|
| Column type     | Metric           |
| Feature level   | Conditional      |
| Allows nulls    | True             |
| Data type       | Decimal          |
| Value format    | Numeric Format |
| Number range    | Any valid decimal value |

## Introduced (version)

1.1

---

# Commitment Discount Status

Commitment Discount Status indicates whether the *charge* corresponds with the consumption of a *commitment discount* identified in the CommitmentDiscountId column or the unused portion of the committed amount. The CommitmentDiscountStatus column is only applicable to *commitment discounts* and not *negotiated discounts*.

## Requirements

CommitmentDiscountStatus adheres to the following requirements:

* CommitmentDiscountStatus MUST be present in a Cost and Usage *FOCUS dataset* when the service provider supports *commitment discounts*.
* CommitmentDiscountStatus MUST be of type String.
* CommitmentDiscountStatus nullability is defined as follows:
  * CommitmentDiscountStatus MUST be null when CommitmentDiscountId is null.
  * CommitmentDiscountStatus MUST NOT be null when CommitmentDiscountId is not null and Charge Category is "Usage".
* CommitmentDiscountStatus MUST be one of the allowed values.

## Column ID

CommitmentDiscountStatus

## Display name

Commitment Discount Status

## Description

Indicates whether the *charge* corresponds with the consumption of a *commitment discount* or the unused portion of the committed amount.

## Content constraints

| Constraint      | Value          |
| :-------------- | :------------- |
| Column type     | Dimension      |
| Feature level   | Conditional    |
| Allows nulls    | True           |
| Data type       | String         |
| Value format    | Allowed Values |

Allowed values:

| Value  | Description                                                             |
| :----- | :---------------------------------------------------------------------- |
| Used   | *Charges* that utilized a specific amount of a commitment discount.     |
| Unused | *Charges* that represent the unused portion of the commitment discount. |

## Introduced (version)

1.0

---

# Commitment Discount Type

Commitment Discount Type is a service-provider-assigned name to identify the type of *commitment discount* applied to the *row*. The CommitmentDiscountType column is only applicable to *commitment discounts* and not *negotiated discounts*.

## Requirements

CommitmentDiscountType adheres to the following requirements:

* CommitmentDiscountType MUST be present in a Cost and Usage *FOCUS dataset* when the service provider supports *commitment discounts*.
* CommitmentDiscountType MUST be of type String.
* CommitmentDiscountType MUST conform to StringHandling requirements.
* CommitmentDiscountType nullability is defined as follows:
  * CommitmentDiscountType MUST be null when CommitmentDiscountId is null.
  * CommitmentDiscountType MUST NOT be null when CommitmentDiscountId is not null.

## Column ID

CommitmentDiscountType

## Display Name

Commitment Discount Type

## Description

A service-provider-assigned identifier for the type of *commitment discount* applied to the *row*.

## Content Constraints

| Constraint      | Value            |
|:----------------|:-----------------|
| Column type     | Dimension        |
| Feature level   | Conditional      |
| Allows nulls    | True             |
| Data type       | String           |
| Value format    | \<not specified> |

## Introduced (version)

1.0-preview

---

# Commitment Discount Unit

Commitment Discount Unit represents the service-provider-specified measurement unit indicating how a service provider measures the Commitment Discount Quantity of a *commitment discount*. The CommitmentDiscountUnit column is only applicable to *commitment discounts* and not *negotiated discounts*.

## Requirements

CommitmentDiscountUnit adheres to the following requirements:

* CommitmentDiscountUnit MUST be present in a Cost and Usage *FOCUS dataset* when the service provider supports *commitment discounts*.
* CommitmentDiscountUnit MUST be of type String.
* CommitmentDiscountUnit MUST conform to StringHandling requirements.
* CommitmentDiscountUnit SHOULD conform to UnitFormat requirements.
* CommitmentDiscountUnit nullability is defined as follows:
  * CommitmentDiscountUnit MUST be null when CommitmentDiscountQuantity is null.
  * CommitmentDiscountUnit MUST NOT be null when CommitmentDiscountQuantity is not null.
* When CommitmentDiscountUnit is not null, CommitmentDiscountUnit adheres to the following additional requirements:
  * CommitmentDiscountUnit MUST remain consistent over time for a given CommitmentDiscountId.
  * CommitmentDiscountUnit MUST represent the unit used to measure the *commitment discount*.
  * When accounting for *commitment discount flexibility*, the CommitmentDiscountUnit value SHOULD reflect this consideration.

See Examples: Commitment Discount Flexibility for more details around *commitment discount flexibility*.

## Column ID

CommitmentDiscountUnit

## Display Name

Commitment Discount Unit

## Description

The service-provider-specified measurement unit indicating how a service provider measures the Commitment Discount Quantity of a *commitment discount*.

## Content constraints

| Constraint      | Value            |
|:----------------|:-----------------|
| Column type     | Dimension        |
| Feature level   | Conditional      |
| Allows nulls    | True             |
| Data type       | String           |
| Value format    | Unit Format|

## Introduced (version)

1.1

---

# Consumed Quantity

The Consumed Quantity represents the volume of a metered SKU associated with a *resource* or *service* used, based on the Consumed Unit. Consumed Quantity is often derived at a finer granularity or over a different time interval when compared to the Pricing Quantity (complementary to Pricing Unit) and focuses on *resource* and *service* consumption, not pricing and cost.

## Requirements

ConsumedQuantity adheres to the following requirements:

* ConsumedQuantity MUST be present in a Cost and Usage *FOCUS dataset* when the service provider supports the measurement of usage.
* ConsumedQuantity MUST be of type Decimal.
* ConsumedQuantity MUST conform to NumericFormat requirements.
* ConsumedQuantity nullability is defined as follows:
  * ConsumedQuantity MUST be null when SkuPriceId is null.
  * ConsumedQuantity MUST be null when ChargeCategory is not "Usage", or when ChargeCategory is "Usage" and CommitmentDiscountStatus is "Unused".
  * When ChargeCategory is "Usage" and CommitmentDiscountStatus is not "Unused", ConsumedQuantity adheres to the following additional requirements:
    * ConsumedQuantity MUST NOT be null when ChargeClass is not "Correction".
    * ConsumedQuantity MAY be null when ChargeClass is "Correction".
* ConsumedQuantity MUST be a valid decimal value when not null.

## Column ID

ConsumedQuantity

## Display Name

Consumed Quantity

## Description

The volume of a metered SKU associated with a *resource* or *service* used, based on the Consumed Unit.

## Content constraints

| Constraint      | Value         |
|:----------------|:--------------|
| Column type     | Metric        |
| Feature level   | Conditional   |
| Allows nulls    | True          |
| Data type       | Decimal       |
| Value format    | Numeric Format |
| Number range    | Any valid decimal value |

## Introduced (version)

1.0

---

# Consumed Unit

The Consumed Unit represents a service-provider-specified measurement unit indicating how a service provider measures usage of a metered SKU associated with a *resource* or *service*. Consumed Unit complements the Consumed Quantity metric. It is often listed at a finer granularity or over a different time interval when compared to Pricing Unit (complementary to Pricing Quantity), and focuses on *resource* and *service* consumption, not pricing and cost.

## Requirements

ConsumedUnit adheres to the following requirements:

* ConsumedUnit MUST be present in a Cost and Usage *FOCUS dataset* when the service provider supports the measurement of usage.
* ConsumedUnit MUST be of type String.
* ConsumedUnit MUST conform to StringHandling requirements.
* ConsumedUnit SHOULD conform to UnitFormat requirements.
* ConsumedUnit nullability is defined as follows:
  * ConsumedUnit MUST be null when ConsumedQuantity is null.
  * ConsumedUnit MUST NOT be null when ConsumedQuantity is not null.

## Column ID

ConsumedUnit

## Display Name

Consumed Unit

## Description

Service-provider-specified measurement unit indicating how a service provider measures usage of a metered SKU associated with a *resource* or *service*.

## Content constraints

|    Constraint   |      Value      |
|:----------------|:----------------|
| Column type     | Dimension       |
| Feature level   | Conditional     |
| Allows nulls    | True            |
| Data type       | String          |
| Value format    | Unit Format recommended |

## Introduced (version)

1.0

---

# Contract Applied

Contract Applied is a set of properties that associate a charge with one or more *contract commitments*, denoted as key-value pairs in a JSON object.  Contract Applied allows the practitioner to track the progress of the commitments to which they have agreed with a service provider.

The FOCUS-defined properties are:

* `Contract ID`: The unique identifier representing a single contract.
* `Contract Commitment ID`: The unique identifier representing a single contract term.
* `Contract Commitment Applied Cost`: The value of the charge applied to a single contract term.
* `Contract Commitment Applied Quantity`: The usage of the charge applied to a single contract term.
* `Contract Commitment Applied Unit`: The unit of measure for the usage of the charge applied to a single contract term.

In addition to these, a data generator may include one or more custom properties, also denoted as key-value pairs.

## Requirements

### Column Requirements

The ContractApplied column adheres to the following requirements:

* ContractApplied MUST be present in a Cost and Usage *FOCUS dataset* when the service provider supports *contract commitments*.
* ContractApplied MUST conform to JsonObjectFormat requirements.
* ContractApplied MUST NOT be null when one or more *contract commitments* are applied to the *charge*.

### Object Schema Requirements

Contract Applied consists of a valid JSON object which contains an array of key-value objects describing the one or more contract commitments applied to the charge. Each object consists of FOCUS-defined keys but can be extended to provide additional details about the contract application.

* If ContractApplied is not null, ContractApplied adheres to the following requirements:
  * ContractApplied MUST have a top-level key "Elements" which contains an array.
  * ContractApplied root object MAY contain custom objects, in addition to "Elements".
  * Each item in "Elements" MUST be an object.
  * "Elements" objects MUST conform to KeyValueFormat requirements.
  * "Elements" objects MUST contain key-value pairs (contract application properties).
  * Contract application property keys SHOULD conform to PascalCase format.
  * "Elements" objects MUST contain four key-value pairs, representing "ContractCommitmentID", "ContractCommitmentAppliedCost", "ContractCommitmentAppliedQuantity", and "ContractCommitmentAppliedUnit".
  * "Elements" objects MAY contain custom key-value pairs, representing additional datapoints provided by the data generator.
  * When custom key-value pairs within "Elements" objects are present:
    * Contract application property custom key-value pairs MUST be prefixed with a consistent `x_` prefix to identify them as external, custom columns and distinguish them from FOCUS columns to avoid conflicts in future releases.
    * Contract application property custom key-value pairs MUST be documented by the data generator.
    * Contract application property custom key-value pairs MUST NOT be nested.
  * FOCUS-defined contract application properties adhere to the following additional requirements:
    * Contract application property key MUST match the spelling and casing specified for the FOCUS-defined property.
    * Contract application property value MUST be of the type specified for that property.
    * Contract application property MUST adhere to additional normative requirements specific to that property.
  * Contract application property keys MUST begin with the string "x_" unless it is a FOCUS-defined allocation property.

### Content Requirements

The following keys are used for contract application properties to facilitate querying data across allocations and across service providers. FOCUS-defined keys will appear in the list below, and custom keys will be prefixed with "x_" to make them easy to identify as well as prevent collisions.

<b>Contract ID</b>

Contract ID is a service-provider-assigned identifier for a contract describing the agreed terms between a service provider and a customer.  Contracts can include commitment to a certain amount of spend or usage over an agreed period of time.

The "ContractId" property adheres to the following requirements:

* "ContractId" MUST be present in a Cost and Usage *FOCUS dataset* when the service provider supports *contract commitments*.
* "ContractId" MUST be of type String.
* "ContractId" MUST conform to StringHandling requirements.
* "ContractId" nullability is defined as follows:
  * "ContractId" MUST be null when a *charge* is not related to a *contract commitment*.
  * "ContractId" MUST NOT be null when a *charge* is related to a *contract commitment*.
* When "ContractId" is not null, "ContractId" adheres to the following additional requirements:
  * "ContractId" MUST be a unique identifier within the service provider.
  * "ContractId" SHOULD be a fully-qualified identifier.

<b>Contract Commitment ID</b>

A Contract Commitment ID is a service-provider-assigned identifier describing an agreement agreed between a service provider and a customer.  Contracts can include commitment to a certain amount of spend or usage over an agreed period of time.

The "ContractCommitmentID" property adheres to the following requirements:

* "ContractCommitmentID" MUST be present in a Cost and Usage *FOCUS dataset* when the service provider supports *contract commitments*.
* "ContractCommitmentID" MUST be of type String.
* "ContractCommitmentID" MUST conform to StringHandling requirements.
* "ContractCommitmentID" nullability is defined as follows:
  * "ContractCommitmentID" MUST be null when a *charge* is not related to a *contract commitment*.
  * "ContractCommitmentID" MUST NOT be null when a *charge* is related to a *contract commitment*.
* When "ContractCommitmentID" is not null, "ContractCommitmentID" adheres to the following additional requirements:
  * "ContractCommitmentID" MUST be a unique identifier within the service provider.
  * "ContractCommitmentID" SHOULD be a fully-qualified identifier.
  * "ContractCommitmentID" MUST have one and only one parent "ContractID".
  * "ContractCommitmentID" MUST be equal to ResourceID when ChargeCategory is "Purchase".
  * "ContractCommitmentID" MAY be equal to "ContractID".

<b>Contract Commitment Applied Cost</b>

Contract Commitment Applied Cost represents the cost of the charge applied to the contract line item.  Contract Commitment Applied Cost is associated with the contract line item via Contract Commitment ID.  Contract Commitment Applied Cost is commonly used for monitoring the progress towards fulfilling contractual commitments that may facilitate discounts for *resources* or *services* as agreed between a service provider and a customer.

The "ContractCommitmentAppliedCost" property adheres to the following requirements:

* "ContractCommitmentAppliedCost" MUST be present in a Cost and Usage *FOCUS dataset* when the service provider associates the *charge's* value with one or more *contract commitments*.
* "ContractCommitmentAppliedCost" MUST be of type Decimal.
* "ContractCommitmentAppliedCost" MUST conform to NumericFormat requirements.
* "ContractCommitmentAppliedCost" nullability is defined as follows:
  * "ContractCommitmentAppliedCost" MUST NOT be null when "ContractCommitmentAppliedQuantity" is null.
  * "ContractCommitmentAppliedCost" MAY be null in all other cases.
* "ContractCommitmentAppliedCost" MUST be a valid decimal value.
* "ContractCommitmentAppliedCost" MUST be denominated in the BillingCurrency.

<b>Contract Commitment Applied Quantity</b>

Contract Commitment Applied Quantity represents the quantity of the charge applied to the contract line item.  Contract Commitment Applied Quantity is associated with the contract line item via Contract Commitment ID.  Contract Commitment Applied Quantity is commonly used for monitoring the progress towards fulfilling contractual commitments that may facilitate discounts for *resources* or *services* as agreed between a service provider and a customer.

The "ContractCommitmentAppliedQuantity" property adheres to the following requirements:

* "ContractCommitmentAppliedQuantity" MUST be present in a Cost and Usage *FOCUS dataset* when the service provider associates the *charge's* quantity with one or more *contract commitments*.
* "ContractCommitmentAppliedQuantity" MUST be of type Decimal.
* "ContractCommitmentAppliedQuantity" MUST conform to NumericFormat requirements.
* "ContractCommitmentAppliedQuantity" nullability is defined as follows:
  * "ContractCommitmentAppliedQuantity" MUST NOT be null when "ContractCommitmentAppliedCost" is null.
  * "ContractCommitmentAppliedQuantity" MAY be null in all other cases.
* "ContractCommitmentAppliedQuantity" MUST be a valid decimal value.
* "ContractCommitmentAppliedQuantity" MUST be denominated in the "ContractCommitmentAppliedUnit".

<b>Contract Commitment Applied Unit</b>

The Contract Commitment Applied Unit represents a service-provider-specified measurement unit for the usage declared in Contract Commitment Applied Quantity. Contract Commitment Applied Unit complements the Contract Commitment Applied Quantity metric.

The "ContractCommitmentAppliedUnit" property adheres to the following requirements:

* "ContractCommitmentAppliedUnit" MUST be present in a Cost and Usage *FOCUS dataset* when the service provider associates the *charge's* quantity with one or more *contract commitments*.
* "ContractCommitmentAppliedUnit" MUST be of type String.
* "ContractCommitmentAppliedUnit" MUST conform to StringHandling requirements.
* "ContractCommitmentAppliedUnit" SHOULD conform to UnitFormat requirements.
* "ContractCommitmentAppliedUnit" nullability is defined as follows:
  * "ContractCommitmentAppliedUnit" MUST be null when "ContractCommitmentAppliedQuantity" is null.
  * "ContractCommitmentAppliedUnit" MUST NOT be null when "ContractCommitmentAppliedQuantity" is not null.

## Overview

### Array of Objects

The parent array is called `Elements` and contains one or more objects which communicate information about how an allocated record was calculated.

| Key | ValueType | Required | Description |
| ----- | ---- | ---------- | ----------- |
| Elements | Array | True | The parent array containing one or more objects which communicate information about how contract commitments were applied to the charge. |

### Object Entries

The `Elements` array contains one or more objects, each of which contains the following entries:

| Key                               | Key Type    | Feature Level | Allows Nulls | Data Type |
| --------------------------------- | ----------- | ------------- | ------------ | --------- |
| ContractID                        | Dimension   | Conditional   | False        | String    |
| ContractCommitmentID              | Dimension   | Conditional   | False        | String    |
| ContractCommitmentAppliedCost     | Dimension   | Conditional   | True         | Numeric   |
| ContractCommitmentAppliedQuantity | Dimension   | Conditional   | True         | Numeric   |
| ContractCommitmentAppliedUnit     | Dimension   | Conditional   | True         | String    |

### Example

```json
{
  "Elements" : [ {
    "ContractID" : "12345",
    "ContractCommitmentID" : "23456",
    "ContractCommitmentAppliedCost" : 500000.00
  }, {
    "ContractID" : "12345",
    "ContractCommitmentID" : "34567",
    "ContractCommitmentAppliedQuantity" : 10000.00,
    "ContractCommitmentAppliedUnit" : "compute_hours"
  } ]
}
```

### JSON Type Definition

```json
{
  "properties": {
    "Elements": {
      "elements": {
        "properties": {
          "ContractID": { "type": "string" },
          "ContractCommitmentID": { "type": "string" }
        },
        "optionalProperties": {
          "ContractCommitmentAppliedCost": { "type": "float64" },
          "ContractCommitmentAppliedQuantity": { "type": "float64" },
          "ContractCommitmentAppliedUnit": { "type": "float64" }
        },
        "additionalProperties": true
      }
    }
  },
  "additionalProperties": true
}
```

NOTE: The above JSON Type Definition (JTD) is an approximation of the expected contents of this column, but it should not be considered normative because it cannot accurately describe the normative requirements (above) for ContractApplied. Where there are discrepancies, deference will be given to the normative requirements. For example, NumericFormat allows for multiple numeric data types and precisions, but JTD requires both to be specified; other numeric data types and precisions allowable under NumericFormat are considered valid.

## Example Scenarios

### Scenario 1: Initial contract commitment

A single Cost and Usage charge represents the values stated on a contract and its three contract commitments agreed between a service provider and a customer:

1) 12345: Spend $500k overall.  (This is the value of the contract, and thus ContractID = ContractCommitmentID.)
2) 23456: Spend $25k on a particular service.
3) 34567: Consume 100k compute hours on a particular resource type.

The Charge Category is denoted as Purchase, and the Contract ID, Resource ID, and Contract Commitment ID are all denoted as 12345.

```json
{
  "ResourceID": "12345",
  "ChargeCategory": "Purchase",
  "BilledCost": 500000.00,
  "EffectiveCost": 0.00,
  "ContractApplied":
    {
      "Elements": [ {
        "ContractID": "12345",
        "ContractCommitmentID": "12345",
        "ContractCommitmentAppliedCost": 500000.00
      }, {
        "ContractID": "12345",
        "ContractCommitmentID": "23456",
        "ContractCommitmentAppliedCost": 25000.00
      }, {
        "ContractID": "12345",
        "ContractCommitmentID": "34567",
        "ContractCommitmentAppliedQuantity": 100000.00,
        "ContractCommitmentAppliedUnit": "compute_hours"
      } ]
    }
```

### Scenario 2: Contract commitment usage with no custom columns

Assume the contract commitment as described in Scenario 1.  Assume that only 50% of cost and usage gets applied to the contract commitments, per the contract terms.

A single Cost and Usage charge for `myResource1` carries Effective Cost of 30 (denominated in USD) and Consumed Quantity of 1 (denominated in compute hours).  The Charge Category is denoted as Usage.

This applies to the contract commitments in the following manner:

```json
{
  "ResourceID": "myResource1",
  "ChargeCategory": "Usage",
  "BilledCost": 0.00,
  "EffectiveCost": 30.00,
  "ConsumedQuantity": 1,
  "ContractApplied":
    {
      "Elements": [ {
        "ContractID": "12345",
        "ContractCommitmentID": "12345",
        "ContractCommitmentAppliedCost": 15.00
      }, {
        "ContractID": "12345",
        "ContractCommitmentID": "23456",
        "ContractCommitmentAppliedCost": 15.00
      }, {
        "ContractID": "12345",
        "ContractCommitmentID": "34567",
        "ContractCommitmentAppliedQuantity": 0.50,
        "ContractCommitmentAppliedUnit": "compute_hours"
      } ]
    }
```

### Scenario 3: Contract commitment usage with custom columns

The same as Scenario 2, except a custom key-value pair `x_ContractCommitmentCostBalance` is provided by the data generator.   This datapoint represents the value remaining on a given contract commitment.

```json
{
  "ResourceID": "myResource1",
  "ChargeCategory": "Usage",
  "BilledCost": 0.00,
  "EffectiveCost": 30.00,
  "ConsumedQuantity": 1,
  "ContractApplied":
    {
      "Elements": [ {
        "ContractID": "12345",
        "ContractCommitmentID": "12345",
        "ContractCommitmentAppliedCost": 15.00,
        "x_ContractCommitmentCostBalance": 499985.00
      }, {
        "ContractID": "12345",
        "ContractCommitmentID": "23456",
        "ContractCommitmentAppliedCost": 15.00,
        "x_ContractCommitmentCostBalance": 24985.00
      }, {
        "ContractID": "12345",
        "ContractCommitmentID": "34567",
        "ContractCommitmentAppliedQuantity": 0.50,
        "ContractCommitmentAppliedUnit": "compute_hours"
      } ]
    }
```

## Column ID

ContractApplied

## Display Name

Contract Applied

## Description

A set of properties that associate a charge with one or more *contract commitments*.

## Content Constraints

| Constraint    | Value                              |
| :------------ | :--------------------------------- |
| Column type   | Dimension and Metric               |
| Feature level | Conditional                        |
| Allows nulls  | True                               |
| Data type     | JSON                               |
| Value format  | JSON Object Format |

## Introduced (version)

1.3

---

# Contracted Cost

Contracted Cost represents the cost calculated by multiplying *contracted unit price* and the corresponding Pricing Quantity. Contracted Cost is denominated in the Billing Currency and is commonly used for calculating savings based on negotiation activities, by comparing it with List Cost. If *negotiated discounts* are not applicable, the Contracted Cost defaults to the List Cost.

## Requirements

ContractedCost adheres to the following requirements:

* ContractedCost MUST be present in a Cost and Usage *FOCUS dataset*.
* ContractedCost MUST be of type Decimal.
* ContractedCost MUST conform to NumericFormat requirements.
* ContractedCost MUST NOT be null.
* ContractedCost MUST be a valid decimal value.
* ContractedCost MUST be denominated in the BillingCurrency.
* When ContractedUnitPrice is null, ContractedCost adheres to the following additional requirements:
  * ContractedCost of a *charge* calculated based on other *charges* (e.g., when the ChargeCategory is "Tax") MUST be calculated based on the ContractedCost of those related *charges*.
  * ContractedCost of a *charge* unrelated to other *charges* (e.g., when the ChargeCategory is "Credit") MUST match the BilledCost.
* ContractedCost MUST equal the product of ContractedUnitPrice and PricingQuantity when ContractedUnitPrice is not null and PricingQuantity is not null.

## Column ID

ContractedCost

## Display Name

Contracted Cost

## Description

Cost calculated by multiplying *contracted unit price* and the corresponding Pricing Quantity.

## Usability Constraints

**Aggregation:** When aggregating Contracted Cost for savings calculations, it's important to exclude either Charge Category "Purchase" *charges* (one-time and recurring) that are paid to cover future eligible *charges* (e.g., commitment discount) or the covered Charge Category "Usage" *charges* themselves. This exclusion helps prevent double counting of these *charges* in the aggregation. Which set of *charges* to exclude depends on whether cost are aggregated on a billed basis (exclude covered *charges*) or accrual basis (exclude Purchases for future *charges*). For instance, *charges* categorized as Charge Category "Purchase" and their related Charge Category "Tax" *charges* for a Commitment Discount might be excluded from an accrual basis cost aggregation of Contracted Cost. This is because the "Usage" and "Tax" charge records provided during the commitment *period* already specify the Contracted Cost. Purchase *charges* that cover future eligible *charges* can be identified by filtering for Charge Category "Purchase" records with a Billed Cost greater than 0 and an Effective Cost equal to 0.

## Content Constraints

| Constraint      | Value                   |
|:----------------|:------------------------|
| Column type     | Metric                  |
| Feature level   | Mandatory               |
| Allows nulls    | False                   |
| Data type       | Decimal                 |
| Value format    | Numeric Format |
| Number range    | Any valid decimal value |

## Introduced (version)

1.0

---

# Contracted Unit Price

The Contracted Unit Price represents the agreed-upon unit price for a single Pricing Unit of the associated SKU, inclusive of *negotiated discounts*, if present, while excluding negotiated *commitment discounts* or any other discounts. This price is denominated in the Billing Currency. The Contracted Unit Price is commonly used for calculating savings based on negotiation activities. If negotiated discounts are not applicable, the Contracted Unit Price defaults to the List Unit Price.

## Requirements

ContractedUnitPrice adheres to the following requirements:

* ContractedUnitPrice MUST be present in a Cost and Usage *FOCUS dataset* when the service provider supports negotiated pricing concepts.
* ContractedUnitPrice adheres to the following additional requirements:
* ContractedUnitPrice MUST be of type Decimal.
* ContractedUnitPrice MUST conform to NumericFormat requirements.
* ContractedUnitPrice nullability is defined as follows:
  * ContractedUnitPrice MUST be null when SkuPriceId is null.
  * ContractedUnitPrice MUST be null when ChargeCategory is "Tax".
  * ContractedUnitPrice MUST NOT be null when SkuPriceId is not null.
  * ContractedUnitPrice MUST NOT be null when ChargeCategory is "Usage" or "Purchase" and ChargeClass is not "Correction".
  * ContractedUnitPrice MAY be null in all other cases.
* When ContractedUnitPrice is not null, ContractedUnitPrice adheres to the following additional requirements:
  * ContractedUnitPrice MUST be a non-negative decimal value.
  * ContractedUnitPrice MUST be denominated in the BillingCurrency.
* ContractedCost MUST equal the product of ContractedUnitPrice and PricingQuantity when ContractedUnitPrice is not null and PricingQuantity is not null.

## Column ID

ContractedUnitPrice

## Display Name

Contracted Unit Price

## Description

The agreed-upon unit price for a single Pricing Unit of the associated SKU, inclusive of negotiated discounts, if present, while excluding negotiated commitment discounts or any other discounts.

## Usability Constraints

**Aggregation:** Column values should only be viewed in the context of their row and not aggregated to produce a total.

## Content Constraints

| Constraint      | Value                                |
|:----------------|:-------------------------------------|
| Column type     | Metric                               |
| Feature level   | Conditional                          |
| Allows nulls    | True                                 |
| Data type       | Decimal                              |
| Value format    | Numeric Format     |
| Number range    | Any valid non-negative decimal value |

## Introduced (version)

1.0

---

# Effective Cost

Effective Cost represents the *amortized* cost of the *charge* after applying all reduced rates, discounts, and the applicable portion of relevant, prepaid purchases (one-time or recurring) that covered this *charge*. The *amortized* portion included should be proportional to the Pricing Quantity and the time granularity of the data. Since amortization breaks down and spreads the cost of a prepaid purchase, to subsequent eligible *charges*, the Effective Cost of the original prepaid *charge* is set to 0. Effective Cost does not mix or "blend" costs across multiple *charges* of the same *service*. This cost is denominated in the Billing Currency. The Effective Cost is commonly utilized to track and analyze spending trends.

This column resolves two challenges that are faced by practitioners:

1. Practitioners need to *amortize* relevant purchases, such as upfront fees, throughout the *commitment* and distribute them to the appropriate reporting groups (e.g., *tags*, *resources*).
2. Many *commitment discount* constructs include a recurring expense for the *commitment* for every *billing period* and must distribute this cost to the *resources* using the *commitment*. This forces reconciliation between the initial *commitment* *row* per period and the actual usage *rows*.

## Requirements

EffectiveCost adheres to the following requirements:

* EffectiveCost MUST be present in a Cost and Usage *FOCUS dataset*.
* EffectiveCost MUST be of type Decimal.
* EffectiveCost MUST conform to NumericFormat requirements.
* EffectiveCost MUST NOT be null.
* EffectiveCost MUST be a valid decimal value.
* EffectiveCost MUST be 0 when ChargeCategory is "Purchase" and the purchase is intended to cover future eligible *charges*.
* EffectiveCost MUST be denominated in the BillingCurrency.
* The sum of EffectiveCost in a given *billing period* MAY differ from the sum of the invoices received for the same *billing period* for a *billing account*.
* When ChargeCategory is not "Usage" or "Purchase", EffectiveCost adheres to the following additional requirements:
  * EffectiveCost of a *charge* calculated based on other *charges* (e.g., when the ChargeCategory is "Tax") MUST be calculated based on the EffectiveCost of those related *charges*.
  * EffectiveCost of a *charge* unrelated to other *charges* (e.g., when the ChargeCategory is "Credit") MUST match the BilledCost.
* *Charges* for a given CommitmentDiscountId adhere to the following additional requirements:
  * The sum of EffectiveCost where ChargeCategory is "Usage" MUST equal the sum of BilledCost where ChargeCategory is "Purchase".
  * The sum of EffectiveCost where ChargeCategory is "Usage" MUST equal the sum of EffectiveCost where ChargeCategory is "Usage" and CommitmentDiscountStatus is "Used", plus the sum of EffectiveCost where ChargeCategory is "Usage" and CommitmentDiscountStatus is "Unused".

## Column ID

EffectiveCost

## Display Name

Effective Cost

## Description

The *amortized* cost of the *charge* after applying all reduced rates, discounts, and the applicable portion of relevant, prepaid purchases (one-time or recurring) that covered this *charge*.

### Concerning Granularity and Distribution of Recurring Fee

Service providers should distribute the *commitment* purchase amount instead of including a *row* at the beginning of a period so practitioners do not need to manually distribute the fee themselves.

### Concerning Amortization Approaches

Eligible purchases should be *amortized* using a methodology determined by the service provider that reflects the needs of their customer base and is proportional to the Pricing Quantity and the time granularity of the *row*. Should a practitioner desire to *amortize* relevant purchases using a different approach, the practitioner can do so using the Billed Cost for the line item representing the initial purchase.

## Content constraints

|    Constraint   |      Value              |
|:----------------|:------------------------|
| Column type     | Metric                  |
| Feature level   | Mandatory               |
| Allows nulls    | False                   |
| Data type       | Decimal                 |
| Value format    | Numeric Format |
| Number range    | Any valid decimal value |

## Introduced (version)

0.5

---

# Host Provider Name

Host Provider Name is the name of the entity that provides the underlying infrastructure on which the *resources* or *services* of the Service Provider are deployed.

In some instances, the host provider and the service provider are the same entity: the provider hosts their own services.  In other instances, the host provider and the service provider are separate entities, though the service provider may or may not expose the host provider and/or allow the customer to select the host provider.

## Requirements

HostProviderName adheres to the following requirements:

* HostProviderName MUST be present in a Cost and Usage *FOCUS dataset*.
* HostProviderName MUST be of type String.
* HostProviderName MUST conform to StringHandling requirements.
* HostProviderName nullability is defined as follows:
  * HostProviderName MAY be NULL when the associated ServiceName does not involve deployment on any underlying infrastructure (e.g., professional services, software licenses).
  * HostProviderName MAY be NULL when the information about the entity providing the underlying infrastructure cannot be uniquely determined (e.g., when the ChargeCategory is "Tax" or "Adjustment").
  * HostProviderName MUST NOT be null in all other cases.
* When HostProviderName is not null, HostProviderName values are defined as follows:
  * HostProviderName MUST reflect the name of the host provider when explicitly selected by the customer.
  * HostProviderName MUST reflect the name of the host provider when the service provider exposes the underlying hosting provider.
  * HostProviderName MUST equal ServiceProviderName in all other cases.

See Appendix: Participating Entity Identification Examples section for examples of Host Provider values across various use case scenarios.

## Column ID

HostProviderName

## Display Name

Host Provider Name

## Description

The name of the entity whose *resources* are used by the Service Provider to make their *resources* or *services* available.

## Content Constraints

| Constraint      | Value            |
|:----------------|:-----------------|
| Column type     | Dimension        |
| Feature level   | Mandatory        |
| Allows nulls    | True             |
| Data type       | String           |
| Value format    | \<not specified> |

## Introduced (version)

1.3

---

# Invoice ID

An Invoice ID is an invoice-issuer-assigned identifier for an invoice encapsulating *charges* in the corresponding *billing period* for a given *billing account*. Invoices are commonly used for scenarios like tracking billing transactions, facilitating payment processes and for performing invoice reconciliation between *charges* and billing periods.

## Requirements

InvoiceId adheres to the following requirements:

* InvoiceId is RECOMMENDED to be present in a Cost and Usage *FOCUS dataset*.
* InvoiceId MUST be of type String.
* InvoiceId MUST conform to StringHandling requirements.
* The sum of BilledCost for a given InvoiceId MUST match the sum of the payable amount provided in the corresponding invoice with the same id generated by the InvoiceIssuerName.
* InvoiceId nullability is defined as follows:
  * InvoiceId MUST be null when the *charge* is not associated either with an invoice or with a pre-generated provisional invoice.
  * InvoiceId MUST NOT be null when the *charge* is associated with either an issued invoice or a pre-generated provisional invoice.
* InvoiceId MAY be generated prior to an invoice being issued.
* InvoiceId MUST be associated with the related *charge* and BillingAccountId when a pre-generated invoice or provisional invoice exists.

See Appendix: Grouping constructs for resources or services for details and examples of the different grouping constructs supported by FOCUS.

## Column ID

InvoiceId

## Display Name

Invoice ID

## Description

The invoice-issuer-assigned identifier for an invoice encapsulating *charges* in the corresponding billing period for a given billing account.

## Content constraints

|    Constraint   |      Value       |
|:----------------|:-----------------|
| Column type     | Dimension        |
| Feature level   | Recommended        |
| Allows nulls    | True            |
| Data type       | String           |
| Value format    | \<not specified> |

## Introduced (version)

1.2

---

# Invoice Issuer Name

Invoice Issuer Name is the name of the entity responsible for issuing payable invoices for the *resources* or *services* consumed. It is commonly used for cost analysis and reporting scenarios.

## Requirements

InvoiceIssuerName adheres to the following requirements:

* InvoiceIssuerName MUST be present in a Cost and Usage *FOCUS dataset*.
* InvoiceIssuerName MUST be of type String.
* InvoiceIssuerName MUST conform to StringHandling requirements.
* InvoiceIssuerName MUST NOT be null.

See Appendix: Participating Entity Identification Examples section for examples of Invoice Issuer Name values across various use case scenarios.

## Column ID

InvoiceIssuerName

## Display Name

Invoice Issuer Name

## Description

The name of the entity responsible for invoicing for the *resources* or *services* consumed.

## Content Constraints

| Constraint      | Value           |
|:----------------|:----------------|
| Column type     | Dimension       |
| Feature level   | Mandatory       |
| Allows nulls    | False           |
| Data type       | String          |
| Value format    | \<not specified> |

## Introduced (version)

0.5

---

# List Cost

List Cost represents the cost calculated by multiplying the *list unit price* and the corresponding Pricing Quantity. List Cost is denominated in the Billing Currency and is commonly used for calculating savings based on various rate optimization activities by comparing it with Contracted Cost, Billed Cost and Effective Cost.

## Requirements

ListCost adheres to the following requirements:

* ListCost MUST be present in a Cost and Usage *FOCUS dataset*.
* ListCost MUST be of type Decimal.
* ListCost MUST conform to NumericFormat requirements.
* ListCost MUST NOT be null.
* ListCost MUST be a valid decimal value.
* ListCost MUST be denominated in the BillingCurrency.
* When ListUnitPrice is null, ListCost adheres to the following additional requirements:
  * ListCost of a *charge* calculated based on other *charges* (e.g., when the ChargeCategory is "Tax") MUST be calculated based on the ListCost of those related *charges*.
  * ListCost of a *charge* unrelated to other *charges* (e.g., when the ChargeCategory is "Credit") MUST match the BilledCost.
* ListCost MUST equal the product of ListUnitPrice and PricingQuantity when ListUnitPrice is not null and PricingQuantity is not null.

## Column ID

ListCost

## Display Name

List Cost

## Description

Cost calculated by multiplying List Unit Price and the corresponding Pricing Quantity.

## Usability Constraints

**Aggregation:** When aggregating List Cost for savings calculations, it's important to exclude either Charge Category "Purchase" *charges* (one-time and recurring) that are paid to cover future eligible *charges* (e.g., commitment discount) or the covered Charge Category "Usage" *charges* themselves. This exclusion helps prevent double counting of these *charges* in the aggregation. Which set of *charges* to exclude depends on whether cost are aggregated on a billed basis (exclude covered *charges*) or accrual basis (exclude Purchases for future *charges*). For instance, *charges* categorized as Charge Category "Purchase" and their related Charge Category "Tax" *charges* for a Commitment Discount might be excluded from an accrual basis cost aggregation of List Cost. This is because the "Usage" and "Tax" charge records provided during the term of the commitment discount already specify the List Cost. Purchase *charges* that cover future eligible *charges* can be identified by filtering for Charge Category "Purchase" records with a Billed Cost greater than 0 and an Effective Cost equal to 0.

## Content Constraints

| Constraint      | Value                   |
|:----------------|:------------------------|
| Column type     | Metric                  |
| Feature level   | Mandatory               |
| Allows nulls    | False                   |
| Data type       | Decimal                 |
| Value format    | Numeric Format |
| Number range    | Any valid decimal value |

## Introduced (version)

1.0-preview

---

# List Unit Price

The List Unit Price represents the suggested service-provider-published unit price for a single Pricing Unit of the associated SKU, exclusive of any discounts. This price is denominated in the Billing Currency. The List Unit Price is commonly used for calculating savings based on various rate optimization activities.

## Requirements

ListUnitPrice adheres to the following requirements:

* ListUnitPrice MUST be present in a Cost and Usage *FOCUS dataset* when the service provider publishes unit prices exclusive of discounts.
* ListUnitPrice MUST be of type Decimal.
* ListUnitPrice MUST conform to NumericFormat requirements.
* ListUnitPrice nullability is defined as follows:
  * ListUnitPrice MUST be null when SkuPriceId is null.
  * ListUnitPrice MUST be null when ChargeCategory is "Tax".
  * ListUnitPrice MUST NOT be null when SkuPriceId is not null.
  * ListUnitPrice MUST NOT be null when ChargeCategory is "Usage" or "Purchase" and ChargeClass is not "Correction".
  * ListUnitPrice MAY be null in all other cases.
* When ListUnitPrice is not null, ListUnitPrice adheres to the following additional requirements:
  * ListUnitPrice MUST be a non-negative decimal value.
  * ListUnitPrice MUST be denominated in the BillingCurrency.
* ListCost MUST equal the product of ListUnitPrice and PricingQuantity when ListUnitPrice is not null and PricingQuantity is not null.

## Column ID

ListUnitPrice

## Display Name

List Unit Price

## Description

The suggested service-provider-published unit price for a single Pricing Unit of the associated SKU, exclusive of any discounts.

## Usability Constraints

**Aggregation:** Column values should only be viewed in the context of their row and not aggregated to produce a total.

## Content Constraints

| Constraint      | Value                                |
|:----------------|:-------------------------------------|
| Column type     | Metric                               |
| Feature level   | Conditional                          |
| Allows nulls    | True                                 |
| Data type       | Decimal                              |
| Value format    | Numeric Format     |
| Number range    | Any valid non-negative decimal value |

## Introduced (version)

1.0-preview

---

# Pricing Category

Pricing Category describes the pricing model used for a *charge* at the time of use or purchase. It can be useful for distinguishing between *charges* incurred at the *list unit price* or a reduced price and exposing optimization opportunities, like increasing *commitment discount* coverage.

## Requirements

PricingCategory adheres to the following requirements:

* PricingCategory MUST be present in a Cost and Usage *FOCUS dataset* when the service provider supports more than one pricing category across all *SKUs*.
* PricingCategory MUST be of type String.
* PricingCategory nullability is defined as follows:
  * PricingCategory MUST be null when SkuPriceId is null.
  * PricingCategory MUST be null when ChargeCategory is "Tax".
  * PricingCategory MUST NOT be null when ChargeCategory is "Usage" or "Purchase" and ChargeClass is not "Correction".
  * PricingCategory MAY be null in all other cases.
* When PricingCategory is not null, PricingCategory adheres to the following additional requirements:
  * PricingCategory MUST be one of the allowed values.
  * PricingCategory MUST be "Standard" when pricing is predetermined at the agreed upon rate for the billing account.
  * PricingCategory MUST be "Committed" when the *charge* is subject to an existing *commitment discount* and is not the purchase of the *commitment discount*.
  * PricingCategory MUST be "Dynamic" when pricing is determined by the service provider and may change over time, regardless of predetermined agreement pricing.
  * PricingCategory MUST be "Other" when there is a pricing model but none of the allowed values apply.

## Column ID

PricingCategory

## Display Name

Pricing Category

## Description

Describes the pricing model used for a *charge* at the time of use or purchase.

## Content constraints

| Constraint      | Value          |
| :-------------- | :------------- |
| Column type     | Dimension      |
| Feature level   | Conditional    |
| Allows nulls    | True           |
| Data type       | String         |
| Value format    | Allowed values |

Allowed values:

| Value     | Description                                                                                                                                                                                                                          |
| :-------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Standard  | *Charges* priced at the agreed upon rate for the billing account, including *negotiated discounts*. This pricing includes any flat rate and volume/tiered pricing but does not include dynamic pricing or reduced pricing due to the application of a *commitment discount*. This does include the purchase of a commitment discount at agreed upon rates. |
| Dynamic   | *Charges* priced at a variable rate determined by the service provider. This includes any product or service with a unit price the service provider can change without notice, like interruptible or low priority *resources*. |
| Committed | *Charges* with reduced pricing due to the application of the *commitment discount* specified by the Commitment Discount ID.                                                                                                          |
| Other     | *Charges* priced in a way not covered by another pricing category.                                                                                                                                                                   |

## Introduced (version)

1.0-preview

---

# Pricing Currency

*Pricing Currency* is the national or virtual currency denomination that a *resource* or *service* was priced in. Pricing Currency is commonly used in scenarios where different currencies are used for pricing and billing.

## Requirements

PricingCurrency adheres to the following requirements:

* PricingCurrency MUST be present in a Cost and Usage *FOCUS dataset* when the service provider supports pricing and billing in different currencies.
* PricingCurrency MUST be of type String.
* PricingCurrency MUST conform to StringHandling requirements.
* PricingCurrency MUST conform to CurrencyFormat requirements.
* PricingCurrency MUST NOT be null.

## Column ID

PricingCurrency

## Display Name

Pricing Currency

## Description

The national or virtual currency denomination that a *resource* or *service* was priced in.

## Content Constraints

| Constraint      | Value                               |
|:----------------|:------------------------------------|
| Column type     | Dimension                           |
| Feature level   | Conditional                         |
| Allows nulls    | True                                |
| Data type       | String                              |
| Value format    | Currency Format |

## Introduced (version)

1.2

---

# Pricing Currency Contracted Unit Price

The Pricing Currency Contracted Unit Price represents the agreed-upon unit price for a single Pricing Unit of the associated *SKU*, inclusive of *negotiated discounts*, if present, while excluding negotiated *commitment discounts* or any other discounts. This price is denominated in the Pricing Currency. When negotiated discounts do not apply to unit prices and instead are applied to exchange rates, the Pricing Currency Contracted Unit Price defaults to the Pricing Currency List Unit Price. The Pricing Currency Contracted Unit Price is commonly used to calculate savings based on negotiation activities.

## Requirements

PricingCurrencyContractedUnitPrice adheres to the following requirements:

* PricingCurrencyContractedUnitPrice presence in a Cost and Usage *FOCUS dataset* is defined as follows:
  * PricingCurrencyContractedUnitPrice MUST be present in a Cost and Usage *FOCUS dataset* when the service provider supports prices in virtual currency and publishes unit prices exclusive of discounts.
  * PricingCurrencyContractedUnitPrice is RECOMMENDED to be present in a Cost and Usage *FOCUS dataset* when the service provider supports pricing and billing in different currencies and publishes unit prices exclusive of discounts.
  * PricingCurrencyContractedUnitPrice MAY be present in a Cost and Usage *FOCUS dataset* in all other cases.
* PricingCurrencyContractedUnitPrice MUST be of type Decimal.
* PricingCurrencyContractedUnitPrice MUST conform to NumericFormat requirements.
* PricingCurrencyContractedUnitPrice nullability is defined as follows:
  * PricingCurrencyContractedUnitPrice MUST be null when SkuPriceId is null.
  * PricingCurrencyContractedUnitPrice MUST be null when ChargeCategory is "Tax".
  * PricingCurrencyContractedUnitPrice MUST NOT be null when SkuPriceId is not null.
  * PricingCurrencyContractedUnitPrice MUST NOT be null when ChargeCategory is "Usage" or "Purchase" and ChargeClass is not "Correction".
  * PricingCurrencyContractedUnitPrice MAY be null in all other cases.
* When PricingCurrencyContractedUnitPrice is not null, PricingCurrencyContractedUnitPrice adheres to the following additional requirements:
  * PricingCurrencyContractedUnitPrice MUST be a non-negative decimal value.
  * PricingCurrencyContractedUnitPrice MUST be denominated in the PricingCurrency.

## Column ID

PricingCurrencyContractedUnitPrice

## Display Name

Pricing Currency Contracted Unit Price

## Description

The agreed-upon unit price for a single Pricing Unit of the associated SKU, inclusive of *negotiated discounts*, if present, while excluding negotiated *commitment discounts* or any other discounts, and expressed in Pricing Currency.

## Usability Constraints

**Aggregation:** Column values should only be viewed in the context of their row and not aggregated to produce a total.

## Content Constraints

| Constraint      | Value                                |
|:----------------|:-------------------------------------|
| Column type     | Metric                               |
| Feature level   | Conditional                          |
| Allows nulls    | True                                 |
| Data type       | Decimal                              |
| Value format    | Numeric Format     |
| Number range    | Any valid non-negative decimal value |

## Introduced (version)

1.2

---

# Pricing Currency Effective Cost

The Pricing Currency Effective Cost represents the cost of the *charge* after applying all reduced rates, discounts, and the applicable portion of relevant, prepaid purchases (one-time or recurring) that covered this *charge*, as denominated in Pricing Currency. This allows the practitioner to perform a conversion from either 1) a *national currency* to a *virtual currency* (e.g., tokens to USD), or 2) one national currency to another (e.g., EUR to USD).

## Requirements

PricingCurrencyEffectiveCost adheres to the following requirements:

* PricingCurrencyEffectiveCost presence in a Cost and Usage *FOCUS dataset* is defined as follows:
  * PricingCurrencyEffectiveCost MUST be present in a Cost and Usage *FOCUS dataset* when the service provider supports prices in virtual currency and publishes unit prices exclusive of discounts.
  * PricingCurrencyEffectiveCost is RECOMMENDED to be present in a Cost and Usage *FOCUS dataset* when the service provider supports pricing and billing in different currencies and publishes unit prices exclusive of discounts.
  * PricingCurrencyEffectiveCost MAY be present in a Cost and Usage *FOCUS dataset* in all other cases.
* PricingCurrencyEffectiveCost MUST be of type Decimal.
* PricingCurrencyEffectiveCost MUST conform to NumericFormat requirements.
* PricingCurrencyEffectiveCost MUST NOT be null.
* PricingCurrencyEffectiveCost MUST be a valid decimal value.
* PricingCurrencyEffectiveCost MUST be 0 in the event of prepaid purchases or purchases that are applicable to previous usage.
* PricingCurrencyEffectiveCost MUST be denominated in the PricingCurrency.

## Column ID

PricingCurrencyEffectiveCost

## Display Name

Pricing Currency Effective Cost

## Description

The cost of the *charge* after applying all reduced rates, discounts, and the applicable portion of relevant, prepaid purchases (one-time or recurring) that covered this *charge*, as denominated in Pricing Currency.

## Content Constraints

|    Constraint   |      Value              |
|:----------------|:------------------------|
| Column type     | Metric                  |
| Feature level   | Conditional             |
| Allows nulls    | True                    |
| Data type       | Decimal                 |
| Value format    | Numeric Format |
| Number range    | Any valid decimal value |

## Introduced (version)

1.2

---

# Pricing Currency List Unit Price

The Pricing Currency List Unit Price represents the suggested service-provider-published unit price for a single Pricing Unit of the associated *SKU*, exclusive of any discounts. This price is denominated in the Pricing Currency. The Pricing Currency List Unit Price is commonly used for calculating savings based on various rate optimization activities.

## Requirements

PricingCurrencyListUnitPrice adheres to the following requirements:

* PricingCurrencyListUnitPrice presence in a Cost and Usage *FOCUS dataset* is defined as follows:
  * PricingCurrencyListUnitPrice MUST be present in a Cost and Usage *FOCUS dataset* when the service provider supports prices in virtual currency and publishes unit prices exclusive of discounts.
  * PricingCurrencyListUnitPrice is RECOMMENDED to be present in a Cost and Usage *FOCUS dataset* when the service provider supports pricing and billing in different currencies and publishes unit prices exclusive of discounts.
  * PricingCurrencyListUnitPrice MAY be present in a Cost and Usage *FOCUS dataset* in all other cases.
* PricingCurrencyListUnitPrice MUST be of type Decimal.
* PricingCurrencyListUnitPrice MUST conform to NumericFormat requirements.
* PricingCurrencyListUnitPrice nullability is defined as follows:
  * PricingCurrencyListUnitPrice MUST be null when SkuPriceId is null.
  * PricingCurrencyListUnitPrice MUST be null when ChargeCategory is "Tax".
  * PricingCurrencyListUnitPrice MUST NOT be null when SkuPriceId is not null.
  * PricingCurrencyListUnitPrice MUST NOT be null when ChargeCategory is "Usage" or "Purchase" and ChargeClass is not "Correction".
  * PricingCurrencyListUnitPrice MAY be null in all other cases.
* When PricingCurrencyListUnitPrice is not null, PricingCurrencyListUnitPrice adheres to the following additional requirements:
  * PricingCurrencyListUnitPrice MUST be a non-negative decimal value.
  * PricingCurrencyListUnitPrice MUST be denominated in the PricingCurrency.

## Column ID

PricingCurrencyListUnitPrice

## Display Name

Pricing Currency List Unit Price

## Description

The suggested service-provider-published unit price for a single Pricing Unit of the associated *SKU*, exclusive of any discounts and expressed in Pricing Currency.

## Usability Constraints

**Aggregation:** Column values should only be viewed in the context of their row and not aggregated to produce a total.

## Content Constraints

| Constraint      | Value                                |
|:----------------|:-------------------------------------|
| Column type     | Metric                               |
| Feature level   | Conditional                          |
| Allows nulls    | True                                 |
| Data type       | Decimal                              |
| Value format    | Numeric Format     |
| Number range    | Any valid non-negative decimal value |

## Introduced (version)

1.2

---

# Pricing Quantity

The Pricing Quantity represents the volume of a given *SKU* associated with a *resource* or *service* used or purchased, based on the Pricing Unit. Distinct from Consumed Quantity (complementary to Consumed Unit), it focuses on pricing and cost, not *resource* and *service* consumption.

## Requirements

PricingQuantity adheres to the following requirements:

* PricingQuantity MUST be present in a Cost and Usage *FOCUS dataset*.
* PricingQuantity MUST be of type Decimal.
* PricingQuantity MUST conform to NumericFormat requirements.
* PricingQuantity nullability is defined as follows:
  * PricingQuantity MUST be null when SkuPriceId is null.
  * PricingQuantity MUST be null when ChargeCategory is "Tax".
  * PricingQuantity MUST NOT be null when ChargeCategory is "Usage" or "Purchase" and ChargeClass is not "Correction".
  * PricingQuantity MAY be null in all other cases.
* PricingQuantity MUST be a valid decimal value when not null.
* Cost metric (e.g., ContractedCost) MUST equal the product of the corresponding unit price (e.g., ContractedUnitPrice) and PricingQuantity when the unit price is not null and PricingQuantity is not null.

## Column ID

PricingQuantity

## Display Name

Pricing Quantity

## Description

The volume of a given *SKU* associated with a *resource* or *service* used or purchased, based on the Pricing Unit.

## Usability Constraints

**Aggregation:** When aggregating Pricing Quantity for commitment utilization calculations, it's important to exclude *commitment discount* purchases (i.e. when Charge Category is "Purchase") that are paid to cover future eligible *charges* (e.g., *commitment discount*). Otherwise, when accounting for all upfront or accrued purchases, it's important to exclude *commitment discount* usage (i.e. when Charge Category is "Usage"). This exclusion helps prevent double counting of these quantities in the aggregation.

## Content Constraints

|    Constraint   |      Value                |
|:----------------|:--------------------------|
| Column type     | Metric                    |
| Feature level   | Mandatory                 |
| Allows nulls    | True                      |
| Data type       | Decimal                   |
| Value format    | Numeric Format |
| Number Range    | Any valid decimal value   |

## Introduced (version)

1.0-preview

---

# Pricing Unit

The Pricing Unit represents a service-provider-specified measurement unit for determining unit prices, indicating how the service provider rates measured usage and purchase quantities after applying pricing rules like *block pricing*. Common examples include the number of hours for compute appliance runtime (e.g., `Hours`), gigabyte-hours for a storage appliance (e.g., `GB-Hours`), or an accumulated count of requests for a network appliance or API service (e.g., `1000 Requests`). Pricing Unit complements the Pricing Quantity metric. Distinct from the Consumed Unit, it focuses on pricing and cost, not *resource* and *service* consumption, often at a coarser granularity.

## Requirements

PricingUnit adheres to the following requirements:

* PricingUnit MUST be present in a Cost and Usage *FOCUS dataset*.
* PricingUnit MUST be of type String.
* PricingUnit MUST conform to StringHandling requirements.
* PricingUnit SHOULD conform to UnitFormat requirements.
* PricingUnit nullability is defined as follows:
  * PricingUnit MUST be null when PricingQuantity is null.
  * PricingUnit MUST NOT be null when PricingQuantity is not null.
* When PricingUnit is not null, PricingUnit adheres to the following additional requirements:
  * PricingUnit MUST be semantically equal to the corresponding pricing measurement unit provided in service-provider-published *price list*.
  * PricingUnit MUST be semantically equal to the corresponding pricing measurement unit provided in invoice, when the invoice includes a pricing measurement unit.

## Column ID

PricingUnit

## Display Name

Pricing Unit

## Description

Service-provider-specified measurement unit for determining unit prices, indicating how the service provider rates measured usage and purchase quantities after applying pricing rules like *block pricing*.

## Content constraints

| Constraint      | Value                   |
|-----------------|-------------------------|
| Column type     | Dimension               |
| Feature level   | Mandatory               |
| Allows nulls    | True                    |
| Data type       | String                  |
| Value format    | Unit Format |

## Introduced (version)

1.0-preview

---

# Provider - DEPRECATED

Provider is the name of the entity that makes the *resources* or *services* available for purchase. It is commonly used for cost analysis and reporting scenarios.

## Requirements

ProviderName adheres to the following requirements:

* ProviderName MUST be present in a Cost and Usage *FOCUS dataset*.
* ProviderName MUST be of type String.
* ProviderName MUST conform to StringHandling requirements.
* ProviderName MUST NOT be null.

See Appendix: Participating Entity Identification Examples section for examples of Service Provider Name, Host Provider Name and Invoice Issuer Name values across various use case scenarios.  For entity identification examples that include the deprecated Provider column, please see [here](https://github.com/FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec/blob/7296e3146fb931ee32b6496fa6e4200e7f4384f7/specification/appendix/origination_of_cost_data.md) (external GitHub link to FOCUS v1.2).

## Column ID

ProviderName

## Display Name

Provider Name

## Description

The name of the entity that made the *resources* or *services* available for purchase.

## Content Constraints

| Constraint      | Value           |
|:----------------|:----------------|
| Column type     | Dimension       |
| Feature level   | Mandatory       |
| Allows nulls    | False           |
| Data type       | String          |
| Value format    | \<not specified> |

## Introduced (version)

0.5

## Deprecated (version)

1.3 Replaced by ServiceProviderName

---

# Publisher - DEPRECATED

Publisher is the name of the entity that produces the *resources* or *services* that were purchased. It is commonly used for cost analysis and reporting scenarios.

## Requirements

PublisherName adheres to the following requirements:

* PublisherName MUST be present in a Cost and Usage *FOCUS dataset*.
* PublisherName MUST be of type String.
* PublisherName MUST conform to StringHandling requirements.
* PublisherName MUST NOT be null.

See Appendix: Participating Entity Identification Examples section for examples of Service Provider Name, Host Provider Name and Invoice Issuer Name values across various use case scenarios.  For entity identification examples that include the deprecated Publisher column, please see [here](https://github.com/FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec/blob/7296e3146fb931ee32b6496fa6e4200e7f4384f7/specification/appendix/origination_of_cost_data.md) (external GitHub link to FOCUS v1.2).

## Column ID

PublisherName

## Display Name

Publisher Name

## Description

The name of the entity that produced the *resources* or *services* that were purchased.

## Content Constraints

| Constraint      | Value           |
|:----------------|:----------------|
| Column type     | Dimension       |
| Feature level   | Mandatory       |
| Allows nulls    | False           |
| Data type       | String          |
| Value format    | \<not specified> |

## Introduced (version)

0.5

## Deprecated (version)

1.3

---

# Region ID

A Region ID is a host-provider-assigned identifier for an isolated geographic area where a *resource* is provisioned or a *service* is provided. The region is commonly used for scenarios like analyzing cost and unit prices based on where *resources* are deployed.

## Requirements

RegionId adheres to the following requirements:

* RegionId MUST be present in a Cost and Usage *FOCUS dataset* when the host provider supports deploying resources or services within a region.
* RegionId MUST be of type String.
* RegionId MUST conform to StringHandling requirements.
* RegionId nullability is defined as follows:
  * RegionId MUST NOT be null when a *resource* or *service* is operated in or managed from a distinct region.
  * RegionId MAY be null when a *resource* or *service* is not operated in or managed from a distinct region.

## Column ID

RegionId

## Display Name

Region ID

## Description

Host-provider-assigned identifier for an isolated geographic area where a *resource* is provisioned or a *service* is provided.

## Content constraints

| Constraint      | Value           |
|-----------------|-----------------|
| Column type     | Dimension       |
| Feature level   | Conditional     |
| Allows nulls    | True            |
| Data type       | String          |
| Value format    | \<not specified> |

## Introduced (version)

1.0

---

# Region Name

Region Name is a host-provider-assigned display name for an isolated geographic area where a *resource* is provisioned or a *service* is provided. Region Name is commonly used for scenarios like analyzing cost and unit prices based on where *resources* are deployed.

## Requirements

RegionName adheres to the following requirements:

* RegionName MUST be present in a Cost and Usage *FOCUS dataset* when the host provider supports deploying resources or services within a region.
* RegionName MUST be of type String.
* RegionName MUST conform to StringHandling requirements.
* RegionName nullability is defined as follows:
  * RegionName MUST be null when RegionId is null.
  * RegionName MUST NOT be null when RegionId is not null.

## Column ID

RegionName

## Display Name

Region Name

## Description

The name of an isolated geographic area where a *resource* is provisioned or a *service* is provided.

## Content constraints

| Constraint      | Value           |
|-----------------|-----------------|
| Column type     | Dimension       |
| Feature level   | Conditional     |
| Allows nulls    | True            |
| Data type       | String          |
| Value format    | \<not specified> |

## Introduced (version)

1.0

---

# Resource ID

A Resource ID is an identifier assigned to a *resource* by the service provider. The Resource ID is commonly used for cost reporting, analysis, and allocation scenarios.

## Requirements

ResourceId adheres to the following requirements:

* ResourceId MUST be present in a Cost and Usage *FOCUS dataset* when the service provider supports billing based on provisioned *resources*.
* ResourceId MUST be of type String.
* ResourceId MUST conform to StringHandling requirements.
* ResourceId nullability is defined as follows:
  * ResourceId MUST be null when a *charge* is not related to a *resource*.
  * ResourceId MUST NOT be null when a *charge* is related to a *resource*.
* When ResourceId is not null, ResourceId adheres to the following additional requirements:
  * ResourceId MUST be a unique identifier within the service provider.
  * ResourceId SHOULD be a fully-qualified identifier.

## Column ID

ResourceId

## Display Name

Resource ID

## Description

Identifier assigned to a *resource* by the service provider.

## Content Constraints

| Constraint      | Value           |
|:----------------|:----------------|
| Column type     | Dimension       |
| Feature level   | Conditional     |
| Allows nulls    | True            |
| Data type       | String          |
| Value format    | \<not specified> |

## Introduced (version)

0.5

---

# Resource Name

The Resource Name is a display name assigned to a *resource*. It is commonly used for cost analysis, reporting, and allocation scenarios.

## Requirements

ResourceName adheres to the following requirements:

* ResourceName MUST be present in a Cost and Usage *FOCUS dataset* when the service provider supports billing based on provisioned resources.
* ResourceName MUST be of type String.
* ResourceName MUST conform to StringHandling requirements.
* ResourceName nullability is defined as follows:
  * ResourceName MUST be null when ResourceId is null or when the *resource* does not have an assigned display name.
  * ResourceName MUST NOT be null when ResourceId is not null and the *resource* has an assigned display name.
* ResourceName MUST NOT duplicate ResourceId when the *resource* is not provisioned interactively or only has a system-generated ResourceId.

## Column ID

ResourceName

## Display Name

Resource Name

## Description

Display name assigned to a *resource*.

## Content Constraints

|    Constraint   |      Value      |
|:----------------|:----------------|
| Column type     | Dimension       |
| Feature level   | Conditional     |
| Allows nulls    | True            |
| Data type       | String          |
| Value format    | \<not specified> |

## Introduced (version)

0.5

---

# Resource Type

Resource Type describes the kind of *resource* the *charge* applies to. A Resource Type is commonly used for scenarios like identifying cost changes in groups of similar *resources* and may include values like Virtual Machine, Data Warehouse, and Load Balancer.

## Requirements

ResourceType adheres to the following requirements:

* ResourceType MUST be present in a Cost and Usage *FOCUS dataset* when the service provider supports billing based on provisioned *resources* and supports assigning types to *resources*.
* ResourceType MUST be of type String.
* ResourceType MUST conform to StringHandling requirements.
* ResourceType nullability is defined as follows:
  * ResourceType MUST be null when ResourceId is null.
  * ResourceType MUST NOT be null when ResourceId is not null.

## Column ID

ResourceType

## Display Name

Resource Type

## Description

The kind of *resource* the *charge* applies to.

## Content Constraints

|    Constraint   |      Value      |
|:----------------|:----------------|
| Column type     | Dimension       |
| Feature level   | Conditional     |
| Allows nulls    | True            |
| Data type       | String          |
| Value format    | \<not specified> |

## Introduced (version)

1.0-preview

---

# Service Category

The Service Category is the highest-level classification of a *service* based on the core function of the *service*. Each *service* should have one and only one category that best aligns with its primary purpose. The Service Category is commonly used for scenarios like analyzing costs across service providers and tracking the migration of workloads across fundamentally different architectures.

## Requirements

ServiceCategory adheres to the following requirements:

* ServiceCategory MUST be present in a Cost and Usage *FOCUS dataset*.
* ServiceCategory MUST be of type String.
* ServiceCategory MUST NOT be null.
* ServiceCategory MUST be one of the allowed values.

## Column ID

ServiceCategory

## Display Name

Service Category

## Description

Highest-level classification of a *service* based on the core function of the *service*.

## Content Constraints

| Constraint      | Value          |
| :-------------- | :------------- |
| Column type     | Dimension      |
| Feature level   | Mandatory      |
| Allows nulls    | False          |
| Data type       | String         |
| Value format    | Allowed Values |

Allowed values:

| Service Category          | Description                                                                                    |
| :------------------------ | :--------------------------------------------------------------------------------------------- |
| AI and Machine Learning   | Artificial Intelligence and Machine Learning related technologies.                             |
| Analytics                 | Data processing, analytics, and visualization capabilities.                                    |
| Business Applications     | Business and productivity applications and services.                                           |
| Compute                   | Virtual, containerized, serverless, or high-performance computing infrastructure and services. |
| Databases                 | Database platforms and services that allow for storage and querying of data.                   |
| Developer Tools           | Software development and delivery tools and services.                                          |
| Multicloud                | Support for interworking of multiple cloud and/or on-premises environments.                    |
| Identity                  | Identity and access management services.                                                       |
| Integration               | Services that allow applications to interact with one another.                                 |
| Internet of Things        | Development and management of IoT devices and networks.                                        |
| Management and Governance | Management, logging, and observability of a customer's use of cloud.                           |
| Media                     | Media and entertainment streaming and processing services.                                     |
| Migration                 | Moving applications and data to the cloud.                                                     |
| Mobile                    | Services enabling cloud applications to interact via mobile technologies.                      |
| Networking                | Network connectivity and management.                                                           |
| Security                  | Security monitoring and compliance services.                                                   |
| Storage                   | Storage services for structured or unstructured data.                                          |
| Web                       | Services enabling cloud applications to interact via the Internet.                             |
| Other                     | New or emerging services that do not align with an existing category.                          |

## Introduced (version)

0.5

---

# Service Name

A *service* represents an offering that can be purchased from a service provider (e.g., cloud virtual machine, SaaS database, professional services from a systems integrator). A *service* offering can include various types of usage or other *charges*. For example, a cloud database *service* may include compute, storage, and networking *charges*.

The Service Name is a display name for the offering that was purchased. The Service Name is commonly used for scenarios like analyzing aggregate cost trends over time and filtering data to investigate anomalies.

## Requirements

ServiceName adheres to the following requirements:

* ServiceName MUST be present in a Cost and Usage *FOCUS dataset*.
* ServiceName MUST be of type String.
* ServiceName MUST conform to StringHandling requirements.
* ServiceName MUST NOT be null.
* The relationship between ServiceName and ServiceCategory is defined as follows:
  * ServiceName MUST have one and only one ServiceCategory that best aligns with its primary purpose, except when no suitable ServiceCategory is available.
  * ServiceName MUST be associated with the ServiceCategory "Other" when no suitable ServiceCategory is available.
* The relationship between ServiceName and ServiceSubcategory is defined as follows:
  * ServiceName SHOULD have one and only one ServiceSubcategory that best aligns with its primary purpose, except when no suitable ServiceSubcategory is available.
  * ServiceName SHOULD be associated with the ServiceSubcategory "Other" when no suitable ServiceSubcategory is available.

## Column ID

ServiceName

## Display Name

Service Name

## Description

An offering that can be purchased from a service provider (e.g., cloud virtual machine, SaaS database, professional *services* from a systems integrator).

## Content Constraints

| Constraint      | Value            |
| :-------------- | :--------------- |
| Column type     | Dimension        |
| Feature level   | Mandatory        |
| Allows nulls    | False            |
| Data type       | String           |
| Value format    | \<not specified> |

## Introduced (version)

0.5

---

# Service Provider Name

Service Provider Name is the name of the entity that provides the *resources* or *services* available for usage or purchase. These services can be built on top of infrastructure provided by a Host Provider, offered as fully integrated solutions, or include complementary offerings such as support, licensing, or consulting. It is commonly used for cost analysis and reporting scenarios.

**Notes:**
* In marketplace scenarios, the Service Provider represents the seller rather than the marketplace operator, as the marketplace operator merely provides a purchasing mechanism and does not itself provide the *resources* or *services* available for usage or purchase.
* In reseller scenarios, if the reseller is selling resource or services that are white-labeled from another provider, the Service Provider is the reseller. In all other cases the Service Provider is the entity that produced the resources or services.

## Requirements

ServiceProviderName adheres to the following requirements:

* ServiceProviderName MUST be present in a Cost and Usage *FOCUS dataset*.
* ServiceProviderName MUST be of type String.
* ServiceProviderName MUST conform to StringHandling requirements.
* ServiceProviderName MUST NOT be null.

See Appendix: Participating Entity Identification Examples section for examples of Service Provider Name values across various use case scenarios.

## Column ID

ServiceProviderName

## Display Name

Service Provider Name

## Description

The name of the entity that made the *resources* or *services* available for purchase or consumption.

## Content Constraints

| Constraint      | Value           |
|:----------------|:----------------|
| Column type     | Dimension       |
| Feature level   | Mandatory       |
| Allows nulls    | False           |
| Data type       | String          |
| Value format    | \<not specified> |

## Introduced (version)

1.3 Introduced as a replacement for ProviderName

---

# Service Subcategory

The Service Subcategory is a secondary classification of the Service Category for a *service* based on its core function. The Service Subcategory (in conjunction with the Service Category) is commonly used for scenarios like analyzing spend and usage for specific workload types across service providers and tracking the migration of workloads across fundamentally different architectures.

## Requirements

ServiceSubcategory adheres to the following requirements:

* ServiceSubcategory is RECOMMENDED to be present in a Cost and Usage *FOCUS dataset*.
* ServiceSubcategory MUST be of type String.
* ServiceSubcategory MUST NOT be null.
* ServiceSubcategory MUST be one of the allowed values.
* ServiceSubcategory MUST have one and only one parent ServiceCategory as specified in the allowed values below.

## Column ID

ServiceSubcategory

## Display Name

Service Subcategory

## Description

Secondary classification of the Service Category for a *service* based on its core function.

## Content Constraints

| Constraint      | Value          |
| :-------------- | :------------- |
| Column type     | Dimension      |
| Feature level   | Recommended    |
| Allows nulls    | False          |
| Data type       | String         |
| Value format    | Allowed Values |

Allowed values:

| Service Category          | Service Subcategory                   | Service Subcategory Description                                                                               |
| ------------------------- | ------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| AI and Machine Learning   | AI Platforms                          | Unified solution that combines artificial intelligence and machine learning technologies.                     |
| AI and Machine Learning   | Bots                                  | Automated performance of tasks such as customer service, data collection, and content moderation.             |
| AI and Machine Learning   | Generative AI                         | Creation of content like text, images, and music by learning patterns from existing data.                     |
| AI and Machine Learning   | Machine Learning                      | Creation, training, and deployment of statistical algorithms that learn from and perform tasks based on data. |
| AI and Machine Learning   | Natural Language Processing           | Generation of human language, handling tasks like translation, sentiment analysis, and text summarization.    |
| AI and Machine Learning   | Other (AI and Machine Learning)       | AI and Machine Learning services that do not fall into one of the defined subcategories.                      |
| Analytics                 | Analytics Platforms                   | Unified solution that combines technologies across the entire analytics lifecycle.                            |
| Analytics                 | Business Intelligence                 | Semantic models, dashboards, reports, and data visualizations to track performance and identify trends.       |
| Analytics                 | Data Processing                       | Integration and transformation tasks to prepare data for analysis.                                            |
| Analytics                 | Search                                | Discovery of information by indexing and retrieving data from various sources.                                |
| Analytics                 | Streaming Analytics                   | Real-time data stream processes to detect patterns, trends, and anomalies as they occur.                      |
| Analytics                 | Other (Analytics)                     | Analytics services that do not fall into one of the defined subcategories.                                    |
| Business Applications     | Productivity and Collaboration        | Tools that facilitate individuals managing tasks and working together.                                        |
| Business Applications     | Other (Business Applications)         | Business Applications services that do not fall into one of the defined subcategories.                        |
| Compute                   | Containers                            | Management and orchestration of containerized compute platforms.                                              |
| Compute                   | End User Computing                    | Virtualized desktop infrastructure and device / endpoint management.                                          |
| Compute                   | Quantum Compute                       | Resources and simulators that leverage the principles of quantum mechanics.                                   |
| Compute                   | Serverless Compute                    | Enablement of compute capabilities without provisioning or managing servers.                                  |
| Compute                   | Virtual Machines                      | Computing environments ranging from hosts with abstracted operating systems to bare-metal servers.            |
| Compute                   | Other (Compute)                       | Compute services that do not fall into one of the defined subcategories.                                      |
| Databases                 | Caching                               | Low-latency and high-throughput access to frequently accessed data.                                           |
| Databases                 | Data Warehouses                       | Big data storage and querying capabilities.                                                                   |
| Databases                 | Ledger Databases                      | Immutable and transparent databases to record tamper-proof and cryptographically secure transactions.         |
| Databases                 | NoSQL Databases                       | Unstructured or semi-structured data storage and querying capabilities.                                       |
| Databases                 | Relational Databases                  | Structured data storage and querying capabilities.                                                            |
| Databases                 | Time Series Databases                 | Time-stamped data storage and querying capabilities.                                                          |
| Databases                 | Other (Databases)                     | Database services that do not fall into one of the defined subcategories.                                     |
| Developer Tools           | Developer Platforms                   | Unified solution that combines technologies across multiple areas of the software development lifecycle.      |
| Developer Tools           | Continuous Integration and Deployment | CI/CD tools and services that support building and deploying code for software and systems.                   |
| Developer Tools           | Development Environments              | Tools and services that support authoring code for software and systems.                                      |
| Developer Tools           | Source Code Management                | Tools and services that support version control of code for software and systems.                             |
| Developer Tools           | Quality Assurance                     | Tools and services that support testing code for software and systems.                                        |
| Developer Tools           | Other (Developer Tools)               | Developer Tools services that do not fall into one of the defined subcategories.                              |
| Identity                  | Identity and Access Management        | Technologies that ensure users have appropriate access to resources.                                          |
| Identity                  | Other (Identity)                      | Identity services that do not fall into one of the defined subcategories.                                     |
| Integration               | API Management                        | Creation, publishing, and management of application programming interfaces.                                   |
| Integration               | Messaging                             | Asynchronous communication between distributed applications.                                                  |
| Integration               | Workflow Orchestration                | Design, execution, and management of business processes and workflows.                                        |
| Integration               | Other (Integration)                   | Integration services that do not fall into one of the defined subcategories.                                  |
| Internet of Things        | IoT Analytics                         | Examination of data collected from IoT devices.                                                               |
| Internet of Things        | IoT Platforms                         | Unified solution that combines IoT data collection, processing, visualization, and device management.         |
| Internet of Things        | Other (Internet of Things)            | Internet of Things (IoT) services that do not fall into one of the defined subcategories.                     |
| Management and Governance | Architecture                          | Planning, design, and construction of software systems.                                                       |
| Management and Governance | Compliance                            | Adherance to regulatory standards and industry best practices.                                                |
| Management and Governance | Cost Management                       | Monitoring and controlling expenses of systems and services.                                                  |
| Management and Governance | Data Governance                       | Management of the availability, usability, integrity, and security of data.                                   |
| Management and Governance | Disaster Recovery                     | Plans and procedures that ensure systems and services can recover from disruptions.                           |
| Management and Governance | Endpoint Management                   | Tools that configure and secure access to devices.                                                            |
| Management and Governance | Observability                         | Monitoring, logging, and tracing of data to track the performance and health of systems.                      |
| Management and Governance | Support                               | Assistance and expertise supplied by service providers.                                                       |
| Management and Governance | Other (Management and Governance)     | Management and governance services that do not fall into one of the defined subcategories.                    |
| Media                     | Content Creation                      | Production of media content.                                                                                  |
| Media                     | Gaming                                | Development and delivery of gaming services.                                                                  |
| Media                     | Media Streaming                       | Multimedia delivered and rendered in real-time on devices.                                                    |
| Media                     | Mixed Reality                         | Technologies that blend real-world and computer-generated environments.                                       |
| Media                     | Other (Media)                         | Media services that do not fall into one of the defined subcategories.                                        |
| Migration                 | Data Migration                        | Movement of stored data from one location to another.                                                         |
| Migration                 | Resource Migration                    | Movement of resources from one location to another.                                                           |
| Migration                 | Other (Migration)                     | Migration services that do not fall into one of the defined subcategories.                                    |
| Mobile                    | Other (Mobile)                        | All Mobile services.                                                                                          |
| Multicloud                | Multicloud Integration                | Environments that facilitate consumption of services from multiple cloud service providers.                   |
| Multicloud                | Other (Multicloud)                    | Multicloud services that do not fall into one of the defined subcategories.                                   |
| Networking                | Application Networking                | Distribution of incoming network traffic across application-based workloads.                                  |
| Networking                | Content Delivery                      | Distribution of digital content using a network of servers (CDNs).                                            |
| Networking                | Network Connectivity                  | Facilitates communication between networks or network segments.                                               |
| Networking                | Network Infrastructure                | Configuration, monitoring, and troubleshooting of network devices.                                            |
| Networking                | Network Routing                       | Services that select paths for traffic within or across networks.                                             |
| Networking                | Network Security                      | Protection from unauthorized network access and cyber threats using firewalls and anti-malware tools.         |
| Networking                | Other (Networking)                    | Networking services that do not fall into one of the defined subcategories.                                   |
| Security                  | Secret Management                     | Information used to authenticate users and systems, including secrets, certificates, tokens, and other keys.  |
| Security                  | Security Posture Management           | Tools that help organizations configure, monitor, and improve system security.                                |
| Security                  | Threat Detection and Response         | Collect and analyze security data to identify and respond to potential security threats and vulnerabilities.  |
| Security                  | Other (Security)                      | Security services that do not fall into one of the defined subcategories.                                     |
| Storage                   | Backup Storage                        | Secondary storage to protect against data loss.                                                               |
| Storage                   | Block Storage                         | High performance, low latency storage that provides random access.                                            |
| Storage                   | File Storage                          | Scalable, sharable storage for file-based data.                                                               |
| Storage                   | Object Storage                        | Highly available, durable storage for unstructured data.                                                      |
| Storage                   | Storage Platforms                     | Unified solution that supports multiple storage types.                                                        |
| Storage                   | Other (Storage)                       | Storage services that do not fall into one of the defined subcategories.                                      |
| Web                       | Application Platforms                 | Integrated environments that run web applications.                                                            |
| Web                       | Other (Web)                           | Web services that do not fall into one of the defined subcategories.                                          |
| Other                     | Other (Other)                         | Services that do not fall into one of the defined categories.                                                 |

## Introduced (version)

1.1

---

# SKU ID

A SKU ID is a service-provider-specified unique identifier that represents a specific *SKU*. *SKUs* are quantifiable goods or service offerings in a Cost and Usage *FOCUS dataset* that represent specific functionality and technical specifications. Examples of *SKUs* include but are not limited to:

* A product license that is purchased or subscribed to.
* Usage of a deployed resource from direct user interaction (e.g., request count).
* Usage by a deployed resource based on the resource's configuration (e.g., running hours, storage space).

Each SKU ID represents a unique set of features that can be sold at different price points or *SKU Prices*. SKU ID is consistent across all pricing variations, which may differ based on multiple factors beyond the common functionality and technical specifications. Examples include but are not limited to:

* Date the *charge* was incurred.
* Pricing tiers (e.g., free tier or volume-based tiers).
* Commitment discount pricing *period* (e.g., 1 year, 3 years).
* Negotiated discounts or other contractual terms or conditions.

SKU ID should be consistent across pricing variations of a good or service to facilitate price comparisons for the same functionality, like where the functionality is provided or how it's paid for. SKU ID can be referenced on a catalog or *price list* published by a service provider to look up detailed information about the *SKU*. The composition of the properties associated with the SKU ID may differ across service providers. SKU ID is commonly used for analyzing and comparing costs for the same SKU across different price details (e.g., *period*, tier, location).

## Requirements

SkuId adheres to the following requirements:

* SkuId MUST be present in a Cost and Usage *FOCUS dataset* when the service provider supports unit pricing concepts and publishes price lists, publicly or as part of contracting.
* SkuId MUST be of type String.
* SkuId MUST conform to StringHandling requirements.
* SkuId nullability is defined as follows:
  * SkuId MUST be null when ChargeCategory is "Tax".
  * SkuId MUST NOT be null when ChargeCategory is "Usage" or "Purchase" and ChargeClass is not "Correction".
  * SkuId MAY be null in all other cases.
* SkuId for a given *SKU* adheres to the following additional requirements:
  * SkuId MUST remain consistent across *billing accounts* or contracts.
  * SkuId MUST remain consistent across PricingCategory values.
  * SkuId MUST remain consistent regardless of any other factors that might impact the price but do not affect the functionality of the *SKU*.
* SkuId MUST be associated with a given *resource* or *service* when ChargeCategory is "Usage" or "Purchase".
* SkuId MAY equal SkuPriceId.

## Column ID

SkuId

## Display Name

SKU ID

## Description

Service-provider-specified unique identifier that represents a specific *SKU* (e.g., a quantifiable good or service offering).

## Content constraints

| Constraint    | Value            |
| :------------ | :--------------- |
| Column type   | Dimension        |
| Feature level | Conditional      |
| Allows nulls  | True             |
| Data type     | String           |
| Value format  | \<not specified> |

## Introduced (version)

1.0-preview

---

# SKU Meter

SKU Meter describes the functionality being metered or measured by a particular SKU in a *charge*.

Service providers often have billing models in which multiple SKUs exist for a given service to describe and bill for different functionalities for that service. For example, an object storage service may have separate SKUs for functionalities such as object storage, API requests, data transfer, encryption, and object management. This field helps practitioners understand which functionalities are being metered by the different SKUs that appear in a Cost and Usage *FOCUS dataset*.

## Requirements

SkuMeter adheres to the following requirements:

* SkuMeter MUST be present in a Cost and Usage *FOCUS dataset* when the service provider supports unit pricing concepts and publishes *price lists*, publicly or as part of contracting.
* SkuMeter MUST be of type String.
* SkuMeter MUST conform to StringHandling requirements.
* SkuMeter nullability is defined as follows:
  * SkuMeter MUST be null when SkuId is null.
  * SkuMeter SHOULD NOT be null when SkuId is not null.
* SkuMeter SHOULD remain consistent over time for a given SkuId.

## Examples

Compute Usage, Block Volume Usage, Data Transfer, API Requests

## Column ID

SkuMeter

## Display Name

SKU Meter

## Description

Describes the functionality being metered or measured by a particular SKU in a *charge*.

## Content Constraints

|    Constraint   |      Value       |
|:----------------|:-----------------|
| Column type     | Dimension        |
| Feature level   | Conditional      |
| Allows nulls    | True             |
| Data type       | String           |
| Value format    | \<not specified> |

## Introduced (version)

1.1

---

# SKU Price Details

SKU Price Details represent a list of *SKU Price* properties (key-value pairs) associated with a specific SKU Price ID. These properties include qualitative and quantitative properties of a *SKUs* (e.g., functionality and technical specifications), along with core stable pricing properties (e.g., pricing *periods*, tiers, etc.), excluding dynamic or negotiable pricing elements such as unit price amounts, currency (and related exchange rates), temporal validity (e.g., effective dates), and contract- or negotiation-specific factors (e.g., contract or account identifiers, and negotiable discounts).

The composition of properties associated with a specific *SKU Price* may differ across service providers and across *SKUs* within the same service provider. However, the exclusion of dynamic or negotiable pricing properties should ensure that all *charges* with the same SKU Price ID share the same SKU Price Details, i.e., that SKU Price Details remains consistent across different *billing periods* and *billing accounts* within a service provider.

SKU Price Details helps practitioners understand and distinguish *SKU Prices*, each identified by a SKU Price ID and associated with a used or purchased *resource* or *service*. It can also help determine the quantity of units for a property when it holds a numeric value (e.g., CoreCount), even when its unit differs from the one in which the *SKU* is priced and charged, thus supporting FinOps capabilities such as unit economics. Additionally, the SKU Price Details may be used to analyze costs based on pricing properties such as *periods* and tiers.

## Requirements

SkuPriceDetails adheres to the following requirements:

* SkuPriceDetails MUST be present in a Cost and Usage *FOCUS dataset* when the service provider supports unit pricing concepts and publishes *price lists*, publicly or as part of contracting.
* SkuPriceDetails MUST conform to KeyValueFormat requirements.
* SkuPriceDetails property keys SHOULD conform to PascalCase format.
* SkuPriceDetails nullability is defined as follows:
  * SkuPriceDetails MUST be null when SkuPriceId is null.
  * SkuPriceDetails MAY be null when SkuPriceId is not null.
* When SkuPriceDetails is not null, SkuPriceDetails adheres to the following additional requirements:
  * SkuPriceDetails MUST be associated with a given SkuPriceId.
  * SkuPriceDetails MUST include the FOCUS-defined SKU Price property when an equivalent property is included as a custom property.
  * SkuPriceDetails MUST NOT include properties that are not applicable to the corresponding SkuPriceId.
  * SkuPriceDetails SHOULD include all FOCUS-defined SKU Price properties listed below that are applicable to the corresponding SkuPriceId.
  * SkuPriceDetails SHOULD include all custom SKU Price properties that are applicable to the corresponding SkuPriceId when there is no equivalent FOCUS-defined property.
  * SkuPriceDetails MAY include properties that are already captured in other dedicated columns.
  * SkuPriceDetails properties for a given SkuPriceId adhere to the following additional requirements:
    * Existing SkuPriceDetails properties SHOULD remain consistent over time.
    * Existing SkuPriceDetails properties SHOULD NOT be removed.
    * Additional SkuPriceDetails properties MAY be added over time.
  * Property key SHOULD remain consistent across comparable *SKUs* having that property, and the values for this key SHOULD remain in a consistent format.
  * Property key MUST begin with the string "x_" unless it is a FOCUS-defined property.
  * Property value MUST represent the value for a single PricingUnit when the property holds a numeric value.
* FOCUS-defined SKU Price properties adhere to the following additional requirements:
  * Property key MUST match the spelling and casing specified for the FOCUS-defined property.
  * Property value MUST be of the type specified for that property.
  * Property value MUST represent the value for a single PricingUnit, denominated in the unit of measure specified for that property when the property holds a numeric value.

## Examples

```json
{
    "StorageClass": "Archive",
    "CoreCount": 4,
    "x_PremiumProcessing": true
}
```

## Column ID

SkuPriceDetails

## Display Name

SKU Price Details

## Description

A set of properties of a SKU Price ID which are meaningful and common to all instances of that SKU Price ID.

## Content Constraints

| Constraint    | Value                                |
| :------------ | :----------------------------------- |
| Column type   | Dimension                            |
| Feature level | Conditional                          |
| Allows nulls  | True                                 |
| Data type     | JSON                                 |
| Value format  | Key-Value Format |

### FOCUS-Defined Properties

The following keys should be used when applicable to facilitate cross-SKU and cross-service-provider queries for the same conceptual property. FOCUS-defined keys will appear in the list below and custom (e.g., service-provider-defined) keys will be prefixed with "x_" to make them easy to identify as well as prevent collisions.

| Key                      | Description                                                              | Data Type        | Unit of Measure (numeric) or example values (string)  |
| :----------------------- | :----------------------------------------------------------------------- | :--------------- | :---------------------------------------------------- |
| CoreCount                | Number of physical or virtual CPUs available<sup>1</sup>                 | Numeric          | Measure: Quantity of Cores                            |
| DiskMaxIops              | Storage maximum sustained input/output operations per second<sup>1</sup> | Numeric          | Measure: Input/Output Operations per Second (IOPS)    |
| DiskSpace                | Storage capacity available                                               | Numeric          | Measure: Gibibytes (GiB)                              |
| DiskType                 | Kind of disk used                                                        | String           | Examples: "SSD", "HDD", "NVMe"                        |
| GpuCount                 | Number of GPUs available                                                 | Numeric          | Measure: Quantity of GPUs                             |
| InstanceType             | Common name of the instance including size, shape, series, etc.          | String           | Examples: "m5d.2xlarge", "NC24rs_v3", "P50"           |
| InstanceSeries           | Common name for the series and/or generation of the instance             | String           | Examples: "M5", "Dadv5", "N2D"                        |
| MemorySize               | RAM allocated for processing                                             | Numeric          | Measure: Gibibytes (GiB<sup>2</sup>)                  |
| NetworkMaxIops           | Network maximum sustained input/output operations per second<sup>1</sup> | Numeric          | Measure: Input/Output Operations per Second (IOPS)    |
| NetworkMaxThroughput     | Network maximum sustained throughput for data transfer<sup>1</sup>       | Numeric          | Measure: Megabits per second (Mbps)                   |
| OperatingSystem          | Operating system family<sup>3</sup>                                      | String           | Examples: "Linux", "MacOS", "Windows"                 |
| Redundancy               | Level of redundancy offered by the SKU                                   | String           | Examples: "Local", "Zonal", "Global"                  |
| StorageClass             | Class or tier of storage provided                                        | String           | Examples: "Hot", "Archive", "Nearline"                |

Notes
<br><sup>1</sup> In the case of "burstable" SKUs offering variable levels of performance, the baseline or guaranteed value should be used.
<br><sup>2</sup> Memory manufacturers still commonly uses "GB" to refer to 2<sup>30</sup> bytes, which is known as GiB in other contexts.
<br><sup>3</sup> This is the operating system family of the SKU, if it's included with the SKU or the SKU only supports one type of operating system.

## Introduced (version)

1.1

---

# SKU Price ID

SKU Price ID is a service-provider-specified unique identifier that represents a specific *SKU Price* associated with a *resource* or *service* used or purchased. It serves as a key reference for a *SKU Price* in a *price list* published by a service provider, allowing practitioners to look up detailed information about the *SKU Price*.

The composition of properties associated with the SKU Price ID may differ across service providers and across *SKUs* within the same service provider. However, the exclusion of dynamic or negotiable pricing properties, such as unit price amount, currency (and related exchange rates), temporal validity (e.g., effective dates), and contract- or negotiation-specific elements (e.g., contract or account identifiers, and negotiable discounts), ensures that the SKU Price ID remains consistent across different billing periods and billing accounts within a service provider. This consistency enables efficient filtering of *charges* to track price fluctuations (e.g., changes in unit price amounts) over time and across billing accounts, for both list and contracted unit prices. Additionally, the SKU Price ID is commonly used to analyze costs based on pricing properties such as *periods* and tiers.

## Requirements

SkuPriceId adheres to the following requirements:

* SkuPriceId MUST be present in a Cost and Usage *FOCUS dataset* when the service provider supports unit pricing concepts and publishes *price lists*, publicly or as part of contracting.
* SkuPriceId MUST be of type String.
* SkuPriceId MUST conform to String Handling requirements.
* SkuPriceId nullability is defined as follows:
  * SkuPriceId MUST be null when ChargeCategory is "Tax".
  * SkuPriceId MUST NOT be null when ChargeCategory is "Usage" or "Purchase" and ChargeClass is not "Correction".
  * SkuPriceId MAY be null in all other cases.
* When SkuPriceId is not null, SkuPriceId adheres to the following additional requirements:
  * SkuPriceId MUST have one and only one parent SkuId.
  * SkuPriceId MUST remain consistent over time.
  * SkuPriceId MUST remain consistent across *billing accounts* or contracts.
  * SkuPriceId MAY equal SkuId.
  * SkuPriceId MUST be associated with a given *resource* or *service* when ChargeCategory is "Usage" or "Purchase".
  * SkuPriceId MUST reference a *SKU Price* in a service-provider-supplied *price list*, enabling the lookup of detailed information about the *SKU Price*.
  * SkuPriceId MUST support the lookup of the ListUnitPrice when the service provider publishes unit prices exclusive of discounts.
  * SkuPriceId MUST support the verification of the given ContractedUnitPrice when the service provider supports negotiated pricing concepts.

See Examples: Commitment Discount Flexibility for more details around *commitment discount flexibility*.

## Column ID

SkuPriceId

## Display Name

SKU Price ID

## Description

A service-provider-specified unique identifier that represents a specific *SKU Price* associated with a *resource* or *service* used or purchased.

## Content constraints

| Constraint       | Value          |
| :--------------- | :------------- |
| Column type      | Dimension      |
| Feature level    | Conditional    |
| Allows nulls     | True           |
| Data type        | String         |
| Value format     | \<not specified> |

## Introduced (version)

1.0-preview

---

# Sub Account ID

A Sub Account ID is a service-provider-assigned identifier assigned to a *sub account*. Sub Account ID is commonly used for scenarios like grouping based on organizational constructs, access management needs, and cost allocation strategies.

## Requirements

SubAccountId adheres to the following requirements:

* SubAccountId MUST be present in a Cost and Usage *FOCUS dataset* when the service provider supports a *sub account* construct.
* SubAccountId MUST be of type String.
* SubAccountId MUST conform to StringHandling requirements.
* SubAccountId nullability is defined as follows:
  * SubAccountId MUST be null when a *charge* is not related to a *sub account*.
  * SubAccountId MUST NOT be null when a *charge* is related to a *sub account*.

See Appendix: Grouping constructs for resources or services for details and examples of the different grouping constructs supported by FOCUS.

## Column ID

SubAccountId

## Display Name

Sub Account ID

## Description

An ID assigned to a grouping of *resources* or *services*, often used to manage access and/or cost.

## Content constraints

|    Constraint   |      Value      |
|:----------------|:----------------|
| Column type     | Dimension       |
| Feature level   | Conditional     |
| Allows nulls    | True            |
| Data type       | String          |
| Value format    | \<not specified> |

## Introduced (version)

0.5

---

# Sub Account Name

A Sub Account Name is a display name assigned to a *sub account*. Sub account Name is commonly used for scenarios like grouping based on organizational constructs, access management needs, and cost allocation strategies.

## Requirements

SubAccountName adheres to the following requirements:

* SubAccountName MUST be present in a Cost and Usage *FOCUS dataset* when the service provider supports a *sub account* construct.
* SubAccountName MUST be of type String.
* SubAccountName MUST conform to StringHandling requirements.
* SubAccountName nullability is defined as follows:
  * SubAccountName MUST be null when SubAccountId is null.
  * SubAccountName MUST NOT be null when SubAccountId is not null.

See Appendix: Grouping constructs for resources or services for details and examples of the different grouping constructs supported by FOCUS.

## Column ID

SubAccountName

## Display Name

Sub Account Name

## Description

A name assigned to a grouping of *resources* or *services*, often used to manage access and/or cost.

## Content constraints

| Constraint      | Value           |
|:----------------|:----------------|
| Column type     | Dimension       |
| Feature level   | Conditional     |
| Allows nulls    | True            |
| Data type       | String          |
| Value format    | \<not specified> |

## Introduced (version)

0.5

---

# Sub Account Type

Sub Account Type is a service-provider-assigned name to identify the type of *sub account*. Sub Account Type is a readable display name and not a code. Sub Account Type is commonly used for scenarios like mapping FOCUS and service provider constructs, summarizing costs across service providers, or invoicing and chargeback.

## Requirements

SubAccountType adheres to the following requirements:

* SubAccountType MUST be present in a Cost and Usage *FOCUS dataset* when the service provider supports more than one possible SubAccountType value.
* SubAccountType MUST be of type String.
* SubAccountType MUST conform to StringHandling requirements.
* SubAccountType nullability is defined as follows:
  * SubAccountType MUST be null when SubAccountId is null.
  * SubAccountType MUST NOT be null when SubAccountId is not null.
* SubAccountType MUST be a consistent, readable display value.

## Column ID

SubAccountType

## Display Name

Sub Account Type

## Description

A service-provider-assigned name to identify the type of *sub account*.

## Content Constraints

| Constraint      | Value            |
| :-------------- | :--------------- |
| Column type     | Dimension        |
| Feature level   | Conditional      |
| Allows nulls    | True             |
| Data type       | String           |
| Value format    | \<not specified> |

## Introduced (version)

1.2

---

# Tags

The Tags column represents the set of *tags* assigned to *tag sources* that also account for potential provider-defined or user-defined tag evaluations. Tags are commonly used for scenarios like adding business context to cost and usage data to identify and accurately allocate *charges*. Tags may also be referred to by data generators using other terms such as labels.

A tag becomes *finalized* when a single value is selected from a set of possible tag values assigned to the tag key.  When supported by a data generator, this can occur when a tag value is set by provider-defined or user-defined rules.

## Requirements

Tags adheres to the following requirements:

* Tags MUST be present in a Cost and Usage *FOCUS dataset* when the data generator supports setting user or provider-defined tags.
* Tags MUST conform to KeyValueFormat requirements.
* Tags MAY be null.
* When Tags is not null, Tags adheres to the following additional requirements:
  * Tags MUST include all user-defined and provider-defined tags.
  * Tags MUST only include finalized tags.
  * Tags SHOULD include tag keys with corresponding non-null values for a given *resource*.
  * Tags MAY include tag keys with a null value for a given *resource* depending on the data generator's tag finalization process.
  * Tag keys that do not support corresponding values, MUST have a corresponding true (boolean) value set.
  * Data generator SHOULD publish tag finalization methods and semantics within their respective documentation.
  * Data generator MUST NOT alter tag values unless applying true (boolean) to valueless tags.
* Provider-defined tags adhere to the following additional requirements:
  * Provider-defined tag keys MUST be prefixed with a predetermined, provider-specified tag key prefix that is unique to each corresponding provider-specified tag scheme.
  * Data generator SHOULD publish all provider-specified tag key prefixes within their respective documentation.
* User-defined tags adhere to the following additional requirements:
  * Data generator MUST prefix all but one user-defined tag scheme with a predetermined, provider-specified tag key prefix that is unique to each corresponding user-defined tag scheme when the data generator has more than one user-defined tag scheme.
  * Data generator MUST NOT prefix tag keys when the data generator has only one user-defined tag scheme.
  * Data generator MUST NOT allow reserved tag key prefixes to be used as prefixes for any user-defined tag keys within a prefixless user-defined tag scheme.

## Provider-Defined vs. User-Defined Tags

This example illustrates various tags produced from multiple user-defined and provider-defined tag schemes.  The first three tags illustrate examples from three different, user-defined tag schemes. The data generator predetermined that 1 user-defined tag scheme (i.e., `"foo": "bar"`) does not have a prepended prefix, but the remaining two user-defined tag schemes (i.e., `"userDefinedTagScheme2/foo": "bar"`, `"userDefinedTagScheme3/foo": true`) do have provider-defined and reserved prefixes.  Additionally, the third tag is produced from a valueless, user-defined tag scheme, so the data generator also applies `true` as its default value.

The last two tags illustrate examples from two different, provider-defined tag schemes. Since all provider-defined tag schemes require a prefix, the data generator has prepended predefined and reserved prefixes (`providerDefinedTagScheme1/`, `providerDefinedTagScheme2/`) to each tag.

```json
    {
        "foo": "bar",
        "userDefinedTagScheme2/foo": "bar",
        "userDefinedTagScheme3/foo": true,
        "providerDefinedTagScheme1/foo": "bar",
        "providerDefinedTagScheme2/foo": "bar"
    }
```

## Finalized Tags

Within a data generator, tag keys may be associated with multiple values, and potentially defined at different levels within the data generator, such as accounts, folders, *resource* and other *resource* grouping constructs. When finalizing, *data generator* must reduce these multiple levels of definition to a single value where each key is associated with exactly one value. The method by which this is done and the semantics are up to each data generator but must be documented within their respective documentation.

As an example, let's assume 1 *sub account* exists with 1 virtual machine with the following details, and tag inheritance favors Resources over *Sub Accounts*.

* Sub Account
  * id: *my-sub-account*
  * user-defined tags: *team:ops*, *env:prod*
* Virtual Machine
  * id: *my-vm*
  * user-defined tags: *team:web*

The table below represents a finalized dataset with these *resources*.  It also shows the finalized state after all resource-oriented, tag inheritance rules are processed.

| ResourceType    | ResourceId     | Tags                                        |
| :---------------| :--------------| :-------------------------------------------|
| Sub Account     | my-sub-account | { "team": "ops", "env": "prod" }            |
| Virtual Machine | my-vm          | { "team": "web", *"env": "prod"* }          |

Because the Virtual Machine Resource did not have an `env` tag, it inherited tag, `env:prod` (italicized), from its parent *sub account*.  Conversely, because the Virtual Machine Resource already has a `team` tag (`team:web`), it did not inherit `team:ops` from its parent *sub account*.

## Column ID

Tags

## Display Name

Tags

## Description

The set of tags assigned to *tag sources* that account for potential provider-defined or user-defined tag evaluations.

## Content Constraints

|    Constraint   |      Value       |
|:----------------|:-----------------|
| Column type     | Dimension        |
| Feature level   | Conditional      |
| Allows nulls    | True             |
| Data type       | JSON             |
| Value format    | Key-Value Format |

## Introduced (version)

1.0-preview

---

# Contract Commitment Columns

# Billing Currency

*Billing currency* is an identifier that represents the currency of a *contract commitment*.

## Requirements

BillingCurrency adheres to the following requirements:

* BillingCurrency MUST be present in a Contract Commitment *FOCUS dataset*.
* BillingCurrency MUST be of type String.
* BillingCurrency MUST conform to StringHandling requirements.
* BillingCurrency MUST conform to CurrencyFormat requirements.
* BillingCurrency MUST NOT be null when ContractCommitmentCategory is "Spend".
* BillingCurrency MUST match the currency used in the invoice generated by the invoice issuer.
* BillingCurrency MUST be expressed in *national currency* (e.g., USD, EUR).

## Column ID

BillingCurrency

## Display Name

Billing Currency

## Description

Represents the currency of a *contract commitment*.

## Content Constraints

| Constraint      | Value                               |
|:----------------|:------------------------------------|
| Column type     | Dimension                           |
| Feature level   | Mandatory                           |
| Allows nulls    | True                                |
| Data type       | String                              |
| Value format    | Currency Format  |

## Introduced (version)

1.3

---

# Contract Commitment Category

Contract Commitment Category represents the highest-level classification of a *contract commitment* based on the nature of how it is applied to a charge. Contract Commitment Category is commonly used to identify and distinguish between categories of contract commitments that may require different handling.

## Requirements

ContractCommitmentCategory adheres to the following requirements:

* ContractCommitmentCategory MUST be present in a Contract Commitment *FOCUS dataset*.
* ContractCommitmentCategory MUST be of type String.
* ContractCommitmentCategory MUST NOT be null.
* ContractCommitmentCategory MUST be one of the allowed values.

## Column ID

ContractCommitmentCategory

## Display Name

Contract Commitment Category

## Description

Represents the highest-level classification of a *contract commitment* based on the nature of how it is applied to a charge.

## Content Constraints

| Constraint      | Value          |
| :-------------- | :------------- |
| Column type     | Dimension      |
| Feature level   | Mandatory      |
| Allows nulls    | False          |
| Data type       | String         |
| Value format    | Allowed values |

Allowed values:

| Value   | Description                                                              |
|:--------|:-------------------------------------------------------------------------|
| Spend   | Contract commitments that require a predetermined amount of spend.       |
| Usage   | Contract commitments that require a predetermined amount of usage.       |

## Introduced (version)

1.3

---

# Contract Commitment Cost

Contract Commitment Cost represents the monetary value of the *contract commitment*.  Contract Commitment Cost is commonly used for monitoring the progress towards fulfilling contractual commitments that may facilitate discounts for *resources* or *services* as agreed between a service provider and a customer.

## Requirements

ContractCommitmentCost adheres to the following requirements:

* ContractCommitmentCost MUST be present in a Contract Commitment *FOCUS dataset*.
* ContractCommitmentCost MUST be of type Decimal.
* ContractCommitmentCost MUST conform to NumericFormat requirements.
* ContractCommitmentCost nullability is defined as follows:
  * ContractCommitmentCost MUST NOT be null when ContractCommitmentCategory is "Spend".
  * ContractCommitmentCost MAY be null when ContractCommitmentCategory is "Usage".
* ContractCommitmentCost MUST be a valid decimal value.
* ContractCommitmentCost MUST be denominated in the BillingCurrency.

## Column ID

ContractCommitmentCost

## Display Name

Contract Commitment Cost

## Description

The monetary value of the *contract commitment*.

## Content Constraints

| Constraint    | Value                              |
| :------------ | :--------------------------------- |
| Column type   | Metric                             |
| Feature level | Mandatory                          |
| Allows nulls  | True                               |
| Data type     | Decimal                            |
| Value format  | Numeric Format   |
| Number range  | Any valid decimal value            |

## Introduced (version)

1.3

---

# Contract Commitment Description

Contract Commitment Description provides a high-level context of a *contract commitment* without requiring additional discovery. Contract Commitment Description is a self-contained summary of the contract commitment's terms, which may not be sufficiently described by the other columns of the Contract Commitment dataset.

## Requirements

ContractCommitmentDescription adheres to the following requirements:

* ContractCommitmentDescription MUST be present in a Contract Commitment *FOCUS dataset*.
* ContractCommitmentDescription MUST be of type String.
* ContractCommitmentDescription MUST conform to StringHandling requirements.
* ContractCommitmentDescription SHOULD NOT be null.
* ContractCommitmentDescription maximum length SHOULD be provided in the corresponding FOCUS Metadata Schema.

## Column ID

ContractCommitmentDescription

## Display Name

Contract Commitment Description

## Description

The self-contained summary of the *contract commitment's* terms.

## Content Constraints

|    Constraint   |      Value       |
|:----------------|:-----------------|
| Column type     | Dimension        |
| Feature level   | Mandatory        |
| Allows nulls    | True             |
| Data type       | String           |
| Value format    | \<not specified> |

## Introduced (version)

1.3

---

# Contract Commitment ID

Contract Commitment ID is a service-provider-assigned identifier describing a single contract term agreed between a provider and a customer.  Contracts can include commitments to a certain amount of spend or usage over an agreed period of time.

## Requirements

ContractCommitmentId adheres to the following requirements:

* ContractCommitmentId MUST be present in a Contract Commitment *FOCUS dataset*.
* ContractCommitmentId MUST be of type String.
* ContractCommitmentId MUST conform to StringHandling requirements.
* ContractCommitmentId MUST NOT be null.
* When ContractCommitmentId is not null, ContractCommitmentId adheres to the following additional requirements:
  * ContractCommitmentId MUST be a unique identifier within the service provider.
  * ContractCommitmentId SHOULD be a fully-qualified identifier.
* ContractCommitmentId MUST have one and only one parent ContractId.
* ContractCommitmentId MAY be equal to ContractId.
* ContractCommitmentId MUST be unique across the Contract Commitment dataset.

## Column ID

ContractCommitmentId

## Display Name

Contract Commitment ID

## Description

A service-provider-assigned identifier describing a single contract term agreed between a service provider and a customer.

## Content Constraints

|    Constraint   |      Value       |
|:----------------|:-----------------|
| Column type     | Dimension        |
| Feature level   | Mandatory        |
| Allows nulls    | True             |
| Data type       | String           |
| Value format    | \<not specified> |

## Introduced (version)

1.3

---

# Contract Commitment Period End

Contract Commitment Period End represents the *exclusive end bound* of a *contract commitment period*. For example, a time period where Contract Commitment Period Start is '2024-01-01T00:00:00Z' and Contract Commitment Period End is '2024-01-02T00:00:00Z' includes January 1 2024 since Contract Commitment Period Start represents the *inclusive start bound*, but does not include January 1 2025 since Contract Commitment Period End represents the *exclusive end bound*.

## Requirements

ContractCommitmentPeriodEnd adheres to the following requirements:

* ContractCommitmentPeriodEnd MUST be present in a Contract Commitment *FOCUS dataset*.
* ContractCommitmentPeriodEnd MUST be of type Date/Time.
* ContractCommitmentPeriodEnd MUST conform to DateTimeFormat requirements.
* ContractCommitmentPeriodEnd MUST NOT be null.
* ContractCommitmentPeriodEnd MUST be the *exclusive end bound* of the effective period of the *contract commitment*.

## Column ID

ContractCommitmentPeriodEnd

## Display Name

Contract Commitment Period End

## Description

The *exclusive end bound* of a *contract commitment period*.

## Content constraints

| Constraint      | Value                                |
|:----------------|:-------------------------------------|
| Column type     | Dimension                            |
| Feature level   | Mandatory                            |
| Allows nulls    | False                                |
| Data type       | Date/Time                            |
| Value format    | Date/Time Format |

## Introduced (version)

1.3

---

# Contract Commitment Period Start

Contract Commitment Period Start represents the *inclusive start bound* of a *contract commitment period*. For example, a time period where Contract Commitment Period Start is '2024-01-01T00:00:00Z' and Contract Commitment End is '2025-01-01T00:00:00Z' includes January 1 2024 since Contract Commitment Period Start represents the *inclusive start bound*, but does not include *charges* for January 2 2025 since Contract Commitment Period End represents the *exclusive end bound*.

## Requirements

ContractCommitmentPeriodStart adheres to the following requirements:

* ContractCommitmentPeriodStart MUST be present in a Contract Commitment *FOCUS dataset*.
* ContractCommitmentPeriodStart MUST be of type Date/Time.
* ContractCommitmentPeriodStart MUST conform to DateTimeFormat requirements.
* ContractCommitmentPeriodStart MUST NOT be null.
* ContractCommitmentPeriodStart MUST be the *inclusive start bound* of the effective period of the *contract commitment*.

## Column ID

ContractCommitmentPeriodStart

## Display Name

Contract Commitment Period Start

## Description

The *inclusive start bound* of a *contract commitment period*.

## Content constraints

| Constraint      | Value                                |
|:----------------|:-------------------------------------|
| Column type     | Dimension                            |
| Feature level   | Mandatory                            |
| Allows nulls    | False                                |
| Data type       | Date/Time                            |
| Value format    | Date/Time Format |

## Introduced (version)

1.3

---

# Contract Commitment Quantity

Contract Commitment Quantity represents the amount associated with the *contract commitment*, denominated in a service-provider-defined Contract Commitment Unit.  Contract Commitment Quantity is commonly used for monitoring the progress towards fulfilling contractual commitments that may facilitate discounts for *resources* or *services* as agreed between a provider and a customer.

## Requirements

ContractCommitmentQuantity adheres to the following requirements:

* ContractCommitmentQuantity MUST be present in a Contract Commitment *FOCUS dataset*.
* ContractCommitmentQuantity MUST be of type Decimal.
* ContractCommitmentQuantity MUST conform to NumericFormat requirements.
* ContractCommitmentQuantity nullability is defined as follows:
  * ContractCommitmentQuantity MUST NOT be null when ContractCommitmentCategory is "Usage".
  * ContractCommitmentQuantity MAY be null when ContractCommitmentCategory is "Spend".
* ContractCommitmentQuantity MUST be a valid decimal value.

## Column ID

ContractCommitmentQuantity

## Display Name

Contract Commitment Quantity

## Description

The amount associated with the *contract commitment*.

## Content Constraints

| Constraint    | Value                              |
| :------------ | :--------------------------------- |
| Column type   | Metric                             |
| Feature level | Mandatory                          |
| Allows nulls  | True                               |
| Data type     | Decimal                            |
| Value format  | Numeric Format   |
| Number range  | Any valid decimal value            |

## Introduced (version)

1.3

---

# Contract Commitment Type

Contract Commitment Type is a service-provider-assigned name to identify the type of *contract commitment*. Contract Commitment Type is a readable display name and not a code. Contract Commitment Type is commonly used for displaying and aggregating the types of commitments the practitioner has made, stated in service-provider-specific terms.

## Requirements

ContractCommitmentType adheres to the following requirements:

* ContractCommitmentType MUST be present in a Contract Commitment *FOCUS dataset*.
* ContractCommitmentType MUST be of type String.
* ContractCommitmentType MUST conform to StringHandling requirements.
* ContractCommitmentType MUST NOT be null.
* ContractCommitmentType MUST be a consistent, readable display value.

## Column ID

ContractCommitmentType

## Display Name

Contract Commitment Type

## Description

A service-provider-assigned name to identify the type of *contract commitment*.

## Content Constraints

| Constraint      | Value            |
| :-------------- | :--------------- |
| Column type     | Dimension        |
| Feature level   | Mandatory        |
| Allows nulls    | False            |
| Data type       | String           |
| Value format    | \<not specified> |

## Introduced (version)

1.3

---

# Contract Commitment Unit

The Contract Commitment Unit represents a service-provider-specified measurement unit for the amount declared in Contract Commitment Quantity. Contract Commitment Unit complements the Contract Commitment Quantity metric.

## Requirements

ContractCommitmentUnit adheres to the following requirements:

* ContractCommitmentUnit MUST be present in a Contract Commitment *FOCUS dataset*.
* ContractCommitmentUnit MUST be of type String.
* ContractCommitmentUnit MUST conform to StringHandling requirements.
* ContractCommitmentUnit SHOULD conform to UnitFormat requirements.
* ContractCommitmentUnit nullability is defined as follows:
  * ContractCommitmentUnit MUST be null when ContractCommitmentQuantity is null.
  * ContractCommitmentUnit MUST NOT be null when ContractCommitmentQuantity is not null.

## Column ID

ContractCommitmentUnit

## Display Name

Contract Commitment Unit

## Description

A service-provider-specified measurement unit for the amount declared in Contract Commitment Quantity.

## Content Constraints

| Constraint    | Value                              |
| :------------ | :--------------------------------- |
| Column type   | Dimension                          |
| Feature level | Mandatory                          |
| Allows nulls  | True                               |
| Data type     | String                             |
| Value format  | Unit Format recommended |

## Introduced (version)

1.3

---

# Contract ID

Contract ID is a service-provider-assigned identifier for a contract describing the agreed terms between a service provider and a customer.  Contracts can include commitment to a certain amount of spend or usage over an agreed period of time.

## Requirements

ContractId adheres to the following requirements:

* ContractId MUST be present in a Contract Commitment *FOCUS dataset*.
* ContractId MUST be of type String.
* ContractId MUST conform to StringHandling requirements.
* ContractId MUST NOT be null.
* When ContractId is not null, ContractId adheres to the following additional requirements:
  * ContractId MUST be a unique identifier within the service provider.
  * ContractId SHOULD be a fully-qualified identifier.

## Column ID

ContractId

## Display Name

Contract ID

## Description

A service-provider-assigned identifier for a contract describing the agreed terms between a service provider and a customer.

## Content constraints

|    Constraint   |      Value       |
|:----------------|:-----------------|
| Column type     | Dimension        |
| Feature level   | Mandatory        |
| Allows nulls    | True             |
| Data type       | String           |
| Value format    | \<not specified> |

## Introduced (version)

1.3

---

# Contract Period End

Contract Period End represents the *exclusive end bound* of a *contract period*. For example, a time period where Contract Period Start is '2024-01-01T00:00:00Z' and Contract Period End is '2024-01-02T00:00:00Z' includes January 1 2024 since Contract Period Start represents the *inclusive start bound*, but does not include January 1 2025 since Contract Period End represents the *exclusive end bound*.

## Requirements

ContractPeriodEnd adheres to the following requirements:

* ContractPeriodEnd MUST be present in a Contract Commitment *FOCUS dataset*.
* ContractPeriodEnd MUST be of type Date/Time.
* ContractPeriodEnd MUST conform to DateTimeFormat requirements.
* ContractPeriodEnd MUST NOT be null.
* ContractPeriodEnd MUST be the *exclusive end bound* of the effective period of the *contract*.

## Column ID

ContractPeriodEnd

## Display Name

Contract Period End

## Description

The *exclusive end bound* of a *contract period*.

## Content constraints

| Constraint      | Value                                |
|:----------------|:-------------------------------------|
| Column type     | Dimension                            |
| Feature level   | Mandatory                            |
| Allows nulls    | False                                |
| Data type       | Date/Time                            |
| Value format    | Date/Time Format |

## Introduced (version)

1.3

---

# Contract Period Start

Contract Period Start represents the *inclusive start bound* of a *contract period*. For example, a time period where Contract Period Start is '2024-01-01T00:00:00Z' and Contract Period End is '2025-01-01T00:00:00Z' includes January 1 2024 since Contract Period Start represents the *inclusive start bound*, but does not include January 2 2025 since Contract Period End represents the *exclusive end bound*.

## Requirements

ContractPeriodStart adheres to the following requirements:

* ContractPeriodStart MUST be present in a Contract Commitment *FOCUS dataset*.
* ContractPeriodStart MUST be of type Date/Time.
* ContractPeriodStart MUST conform to DateTimeFormat requirements.
* ContractPeriodStart MUST NOT be null.
* ContractPeriodStart MUST be the *inclusive start bound* of the effective period of the *contract*.

## Column ID

ContractPeriodStart

## Display Name

Contract Period Start

## Description

The *inclusive start bound* of a *contract period*.

## Content constraints

| Constraint      | Value                                |
|:----------------|:-------------------------------------|
| Column type     | Dimension                            |
| Feature level   | Mandatory                            |
| Allows nulls    | False                                |
| Data type       | Date/Time                            |
| Value format    | Date/Time Format |

## Introduced (version)

1.3
