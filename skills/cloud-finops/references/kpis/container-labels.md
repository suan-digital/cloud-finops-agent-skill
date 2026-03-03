<!-- Source: finopsfoundation/framework/_data/container-cost-allocation.yml (CC BY 4.0) -->

# Container Cost Allocation Labels

Kubernetes label strategies for container cost allocation, curated by the FinOps Foundation
Containers SIG. Labels are organized by maturity level (Crawl/Walk/Run) and mapped to personas.

## `application`

Label that supports organizing your spend around application architecture hierarchy.

- **Context:** App / Service Hierarchy
- **Maturity:** Crawl
- **Common Resources:** namespace, pod, deployment
- **Aliases:** application, app, application-name, application-id
- **Example:** ACME Fitness
- **Personas:** Executive, Business

## `cost-center`

Cost-centers aligns to a business structure and help define the various areas that are driving the company expenses.

- **Context:** Business organization
- **Maturity:** Crawl
- **Common Resources:** namespace, pod, deployment
- **Aliases:** psp-element, cost-center
- **Example:** Can be seen as alpha-numeric codes
- **Personas:** Finance

## `team`

Team Label help identify groups within an organization that are responsible for this spend.

- **Context:** Business organization
- **Maturity:** Crawl
- **Common Resources:** namespace, pod, deployment
- **Aliases:** team, squad, group, owner, maintainer, contact
- **Example:** [team name] [team id]
- **Personas:** Executive, Business, Engineering, Finance

## `product`

Product label organizes spend to align on the 'products' a firm customer consume. This label helps organize applications and services that support the product.

- **Context:** App / Service Hierarchy
- **Maturity:** Walk
- **Common Resources:** namespace, pod, deployment
- **Aliases:** product, workload, project
- **Example:** ACME Fitness Store, ACME Fitness + Video Streaming
- **Personas:** Business, Finance

## `department`

Department applies to business organization. Some organization use terms like Business Unit. The meaning is very organization dependent.

- **Context:** Business organization
- **Maturity:** Walk
- **Common Resources:** namespace, pod, deployment
- **Aliases:** business-unit, department, business-domain, domain
- **Example:** retail BU, streaming BU
- **Personas:** Business, Finance

## `environment`

Environment support calculating Cost of Good Sold (COGS) and aligns how organization deploy code. e.g. production versus development.

- **Context:** Platform + Operations
- **Maturity:** Walk
- **Common Resources:** namespace, pod, deployment
- **Aliases:** stage, environment, env
- **Example:** dev, staging, prod
- **Personas:** Business, Engineering

## `customer`

Customer label can identify that that are consuming a product/service. This can support multi-tenant environment as well as silo tenant environments.

- **Context:** Business organization
- **Maturity:** Walk
- **Common Resources:** namespace, pod, deployment
- **Aliases:** customer
- **Example:** [customer id] or [customer name]
- **Personas:** Business, Engineering

## `service`

Service label adds a layer to app/service hierarchy around how firms organize product/applications into sub-components.

- **Context:** App / Service Hierarchy
- **Maturity:** Run
- **Common Resources:** pod, deployment
- **Aliases:** service, service-id
- **Example:** Point of Sale, Store Shopping Cart, Store Catalog
- **Personas:** Engineering, Finance

## `component`

Component label adds a layer to app/service hierarchy around how firms organize "Microservice / Component / Function" that support application or services.

- **Context:** App / Service Hierarchy
- **Maturity:** Run
- **Common Resources:** namespace, pod
- **Aliases:** component, tier
- **Example:** database, storage
- **Personas:** Business, Engineering

## `tech-stack`

Tech-stack helps bring context of spend to the view of platform or operations by purpose.

- **Context:** Platform + Operations
- **Maturity:** Run
- **Common Resources:** namespace, pod, deployment
- **Aliases:** stack, servicegroup
- **Example:** observability, build-tools, automation, security
- **Personas:** Business, Engineering, Finance
