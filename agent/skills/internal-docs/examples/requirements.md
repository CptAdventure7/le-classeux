## Instructions
You are being asked either extract or edit information in a requirement document from INO. The document is in xlsx format. The instructions from the xlsx skills apply with the following addition:
- You don't need to extract Configuration tab
- You don't need to extract information about the FOR tab
- You don't need to extract information about Terminology tab
- You don't need to extract information about Exemples tab
- You don't need to extract information about Template SOF tab
- In usage context, line with only UseCase or User in it are considered empty and can be skipped
- Line with node that are only dot like . or .. are considered empty and can be skipped
- Place the extracted jsonl files in a doc/requirements folder. 
- For "Group 1-4" columns: define your grouping names by editing row 3 headers, then mark rows with "x" only (no text) where the grouping applies.
- Requirement status values must be one of: `Accepted`, `Preliminary`, `Abandoned`.
- Status of conformity values must be one of: `Undetermined`, `Compliant`, `Non-compliant`.
- Need status values must be one of: `Need`, `Would like`, `Abandoned`.

## Workflow

1. **Clarify ambiguity**: Ask question when the request is contextually strange, imprecise or incomplete
2. **Work on extracted data**: During a work session, extract data an work on the local jsonl files
3. **Make change to xlsx**: If asked, update the xlsx file.
4. **Review and commit**: If there is not one, create a tab for change log. The Information FOR tab is not an actual change log, just a template change log, do not use it. Set the column as Date / Time / User / Change

## Terminology

## Use cases

Description

## The need described

## Acquisition

...how the system will be acquired by the customer and/or user

## Deployment

...how the system will be put into service by the customer (transition
from the acquisition phase to the use phase)

## Use

...how the system will be used to fulfill its objectives (related to the
mission) in its context of use (by whom, for what?)

## Support

...how the system will be supported during its useful life

## Disposal

...how the system will be removed and decommissioned

## Constraints

...constraints that the system must respect, without which the mission
or certain benefits would not be met.

## Requirement class

Description

## Functional

Qualitative description of system functions or tasks that must be
performed during normal operation. These requirements are often
associated with system verification or software operation.

## Performance

Quantitative description of the extent, quality, and conditions of
execution of a function or task (e.g., rates, speeds). These are
quantitative system performance requirements and are individually
verifiable. Note that there may be more than one performance requirement
associated with a single function, functional requirement, or task.

## Interface

Define how the system should interact or exchange materials, energy or
information with external systems (external interface), or how elements
of the system, including human elements, interact with each other
(internal interface). Interface requirements include physical
connections (physical interfaces) to external systems or internal system
elements supporting interactions or exchanges.

## User-friendliness

Define the quality of use of the system (e.g. effectiveness, efficiency
and measurable satisfaction criteria).

## Operational

Define the operational conditions or properties required for the system
to function or exist. This type of requirements includes human factors,
ergonomics, availability, maintainability, reliability and security.

## Logistic

Define the logistical conditions necessary for the continued use of the
system. These requirements include support (provision of facilities,
level support, support personnel, spare parts, training, technical
documentation, etc.), packaging, handling, shipping, transportation.

## Mode and/or state

Define the different operational modes of the system in service and the
events leading to mode transitions.

## Environment

Define the environmental conditions that the system will face in its
different operating modes. This should address the natural environment
(e.g., wind, rain, temperature, wildlife, salt, dust, radiation, etc.),
induced and/or self-induced environmental effects (e.g., movement,
shock, noise, electromagnetism, thermal, etc.) and threats to the
societal environment (e.g., legal, political, economic, social,
commercial, etc.)

## Physical

Define the weight, volume and dimension constraints applicable to the
elements of the system that compose it.

## Cybersecurity

It defines the main IT security requirements: Connection/access levels.
Create, read, update, and delete (CRUD) levels. Application data access
permission can only be changed by the system data administrator.
Password requirements: length, special characters, expiration, recycling
policies, 2FA. Inactivity timeouts -- Duration, actions, traceability.
System data backed up every X hours and copies stored in a secure
offsite location. Encryption (data in flight and at rest) -- All
external communications between the system data server and clients must
be encrypted. Data classification/system accreditation: All data must be
protectively marked and stored/protected.

## Constraint

Define the boundaries of the options available to the designer of a
solution by imposing immovable boundaries and limits (for example, the
system must integrate an existing or provided system element, or certain
data must be maintained in a specific online repository).

## Policy and regulations

Define relevant and applicable organizational policies or regulatory
requirements that could affect the operation or performance of the
system (e.g., labor policies, reporting to the regulatory body, health
or safety criteria, etc.)

## Cost and time constraint

Define, for example, the cost of a single copy of the system, the
expected delivery date of the first copy, etc.

## SEBOK references

Stakeholder Requirements Definition

## Priority

Description

## Shall have

This category includes the requirements necessary for project success.
These are non-negotiable items that provide the minimum subset of
requirements necessary to have a functional system.

Statements that are true for must-haves include: - There is no point in
completing the project on time without this requirement. - The final
product or software does not provide an effective solution without this
requirement. - The final product or software would not be compliant or
legal without this requirement. - The final product or software would
not be secure without this requirement.

## Should have

This category includes requirements that are important and generally
help to significantly increase the value of the system.

However, they are not absolutely necessary (unlike those in the "must
have" category). In the event that the requirements in this category are
not met, the final system should still work, but may not have the
perception of maximum business value.

Requirements in this category can be used to communicate future
features.

## Could have

This category includes requirements that are desired, but have a much
lower impact when excluded from the project.

As a result, requirements identified by "Might Have" are often the first
that teams overlook: must-haves and "should haves" requirements always
take priority because they have a greater impact on the product.

## It will not be

Requirements labelled by this category are defined by stakeholders as
the least critical and cost-effective requirements, or as being
inappropriate for the project scope. Assigning a requirement to this
category helps to reinforce the focus on the requirements of the other
three categories and can be beneficial in defining the boundaries of the
system and helping to prevent system requirements from drifting
(requirement creep).

Therefore, the requirements in the "Will not have" category are not
planned.

## Inspired and adapted from:

MoSCoW Method

## Verification/Validation method

Description

## Analysis

Technique based on analytical evidence obtained without any intervention
on the submitted item using mathematical or probabilistic calculation,
logical reasoning (including predicate theory), modelling and/or
simulation under defined conditions to show theoretical conformity .
Mainly used when testing under realistic conditions cannot be performed
or is not cost-effective or to capitalize on already existing data and
results.

## Analogy

Technique based on evidence of similar elements to the submitted element
or on experience feedback. It is absolutely necessary to show by
prediction that the context is invariant that the outcomes are
transposable (models, investigations, experience feedback, etc.). The
analogy (or similarity) can only be used if the submitted element is
similar in design, manufacture, and use; equivalent or more stringent
verification actions were used for the similar element, and the intended
operational environment is identical to or less rigorous than the
similar element.

## Demonstration

Technique used to demonstrate correct operation of the submitted element
against operational and observable characteristics without using
physical measurements (no or minimal instrumentation or test equipment).
Demonstration is sometimes called 'field-testing'. It generally consists
of a set of tests selected by the supplier to show that the element
response to stimuli is suitable or to show that operators can perform
their assigned tasks when using the element. Observations are made and
compared with predetermined/expected responses. Demonstration may be
appropriate when requirements or specification are given in statistical
terms (e.g., mean time to repair, average power consumption, etc.).

## Inspection

Technique based on visual or dimensional examination of an element; the
verification relies on the human senses or uses simple methods of
measurement and handling. Inspection is generally non-destructive, and
typically includes the use of sight, hearing, smell, touch, and taste,
simple physical manipulation, mechanical and electrical gauging, and
measurement. No stimuli (tests) are necessary. The technique is used to
check properties or characteristics best determined by observation
(e.g., paint color, weight, documentation, listing of code, etc.).

## Sampling

Technique based on verification of characteristics using samples. The
number, tolerance, and other characteristics must be specified to be in
agreement with the experience feedback.

## Test

Technique performed onto the submitted element by which functional,
measurable characteristics, operability, supportability, or performance
capability is quantitatively verified when subjected to controlled
conditions that are real or simulated. Testing often uses special test
equipment or instrumentation to obtain accurate quantitative data to be
analyzed. Testing involves verifying products and services only when
they are implemented. Consider other techniques earlier in the design
process; analysis and inspections are cost-effective and uncover
potential errors, defects or failures early on.

## SEBOK references

Verification Method
