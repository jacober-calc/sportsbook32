# SPORTSBOOK Statefile

## CONTENTS

1. [Introduction](#1-introduction)
2. [Disclaimer](#2-disclaimer)
3. [Theory of Operations](#3-theory-of-operations)
4. [Variable Definitions](#4-variable-definitions)
5. [Program Descriptions](#5-program-descriptions)
6. [Operating Instructions](#6-operating-instructions)
7. [Example Calculations](#7-example-calculations)
8. [Quick Reference](#8-quick-reference)
9. [Program Listing](#9-program-listing)

---

## 1. INTRODUCTION

This program suite provides sportsbook odds calculations for two-way markets quoted in American odds. The calculator removes the bookmaker's margin from a pair of odds to find each side's fair probability, calculates the profit on a wager, and converts between American and decimal odds.

### 1.1 Purpose

The program enables bettors to:

- Calculate the bookmaker's margin (overround) on a two-way market
- Determine the fair, no-vig probability of each side
- Calculate the profit on a wager at any American odds
- Convert American odds to decimal odds, and decimal odds to American odds

### 1.2 System Requirements

SwissMicros DM32 calculator with RPN operating system. Program requires 131 program steps in 8 labels. No equations, flags, or indirect registers are used.

### 1.3 Install and Download

Copy **SPORTSBOOK.d32** to the `/STATE` folder of the DM32's internal USB disk, then load it from the calculator. Instructions are available [via the DM32 User Manual](https://technical.swissmicros.com/dm32/doc/dm32_user_manual.html#_saving_and_loading_a_state).

---

## 2. DISCLAIMER

### IMPORTANT NOTICE

This program is provided for educational and recreational purposes. It performs arithmetic on odds supplied by the user and does not predict the outcome of any event. The developer (jacober-calc) makes no warranties, express or implied, regarding the accuracy, completeness, or suitability of this program for any particular purpose. Users are responsible for complying with the laws that apply to sports wagering where they live.

---

## 3. THEORY OF OPERATIONS

### 3.1 American Odds

American odds express a price relative to a 100-unit wager:

- **Negative odds** (the favorite) show the stake required to win 100. At −150, a stake of 150 wins 100.
- **Positive odds** (the underdog) show the profit on a stake of 100. At +130, a stake of 100 wins 130.

### 3.2 Key Equations

#### Implied Probability

```
Favorite:   A = F ÷ (F + 100)
Underdog:   B = 100 ÷ (U + 100)
```

Where F is the favorite's odds without the minus sign and U is the underdog's odds.

#### Overround (Bookmaker's Margin)

```
V = (A + B) × 100 − 100
```

The implied probabilities of the two sides total more than 100%. The excess, in percent, is the bookmaker's margin.

#### Fair (No-Vig) Probability

```
Favorite:   A × 100 ÷ (A + B)
Underdog:   B × 100 ÷ (A + B)
```

Dividing each implied probability by their total removes the margin, so the two fair probabilities total exactly 100%.

#### Profit

```
Positive odds:   W = Stake × O ÷ 100
Negative odds:   W = Stake × 100 ÷ |O|
```

W is the profit on a winning wager. The total return is W plus the stake.

#### Odds Conversion

```
American to decimal:   d = O ÷ 100 + 1        (O > 0)
                       d = 1 − 100 ÷ O        (O ≤ 0)

Decimal to American:   O = (d − 1) × 100      (d ≥ 2)
                       O = −100 ÷ (d − 1)     (d < 2)
```

### 3.3 Program Logic Flow

The no-vig program (LBL O) takes the favorite's odds from the Y-register and the underdog's odds from the X-register.

**Program Flow:**
1. Test whether the two odds are equal
   - If YES: go to LBL Z, which returns the overround and 50% for each side
   - If NO: continue to step 2
2. Store the underdog's odds U and the favorite's odds F
3. Calculate the favorite's implied probability A
4. Calculate the underdog's implied probability B
5. Calculate the total implied probability A + B, and the overround V
6. Divide A and B by the total to give each side's fair probability
7. Display results

---

## 4. VARIABLE DEFINITIONS

| Variable | Description |
|----------|-------------|
| **A** | Favorite's implied probability; after LBL O, favorite's fair probability (%) |
| **B** | Underdog's implied probability; after LBL O, underdog's fair probability (%); after LBL P, the stake |
| **F** | Favorite's odds, entered without the minus sign |
| **O** | American odds (LBL P) |
| **U** | Underdog's odds |
| **V** | Overround (%) |
| **W** | Profit on a winning wager |
| **Y** | Total implied probability, A + B (internal use) |

---

## 5. PROGRAM DESCRIPTIONS

### 5.1 LBL O - No-Vig Odds

Calculates the bookmaker's margin on a two-way market and the fair probability of each side. When the two odds are equal, the program branches to LBL Z.

**Inputs:** Y-register: favorite's odds without the minus sign. X-register: underdog's odds.

**Outputs (Stack display from top to bottom):**
- Z: Overround (%)
- Y: Favorite's fair probability (%)
- X: Underdog's fair probability (%)

### 5.2 LBL P - Profit Calculator

Calculates the profit on a winning wager. Negative odds branch to LBL Y.

**Inputs:** Y-register: American odds, with sign. X-register: stake.

**Output:** Profit (stored in W register)

### 5.3 LBL D - American to Decimal Odds

Converts American odds to decimal odds. Negative odds branch to LBL C.

**Input:** X-register: American odds, with sign.

**Output:** Decimal odds in the X-register

### 5.4 LBL A - Decimal to American Odds

Converts decimal odds to American odds. Decimal odds of 2 or greater branch to LBL B.

**Input:** X-register: decimal odds.

**Output:** American odds in the X-register

---

## 6. OPERATING INSTRUCTIONS

All programs take their inputs from the stack. None prompt for input.

### 6.1 No-Vig Odds (LBL O)

**Procedure:**

1. Key in the favorite's odds without the minus sign and press `ENTER`
2. Key in the underdog's odds
3. Press `XEQ O`

**The program will display (from top to bottom on screen):**
- Z-register: Overround (%)
- Y-register: Favorite's fair probability (%)
- X-register: Underdog's fair probability (%)

### 6.2 Profit (LBL P)

**Procedure:**

1. Key in the American odds, with sign, and press `ENTER`
2. Key in the stake
3. Press `XEQ P`

The profit is displayed in the X-register.

### 6.3 Odds Conversion (LBL D and LBL A)

**Procedure:**

1. Key in the odds
2. Press `XEQ D` to convert American to decimal, or `XEQ A` to convert decimal to American

The converted odds are displayed in the X-register.

---

## 7. EXAMPLE CALCULATIONS

Results are shown in FIX 6, the display format saved in the Statefile.

### 7.1 No-Vig Odds

**Scenario:**

A sportsbook quotes the favorite at −150 and the underdog at +130. Find the bookmaker's margin and the fair probability of each side.

**Solution:**

| Keys | Description |
|------|-------------|
| `150` `ENTER` | Favorite's odds, without the minus sign |
| `130` | Underdog's odds |
| `XEQ O` | Runs the program |

**Results (displayed on screen from top to bottom):**

| Register | Value | Meaning |
|----------|-------|---------|
| Z | 3.478261 | 3.48% overround |
| Y | 57.983193 | Favorite's fair probability, 57.98% |
| X | 42.016807 | Underdog's fair probability, 42.02% |

**Interpretation:**

The implied probabilities, 60.00% and 43.48%, total 103.48%. With the margin removed, the favorite has a 57.98% fair probability of winning and the underdog 42.02%.

### 7.2 Equal Odds

**Scenario:**

A sportsbook quotes both sides of a point spread at −110.

**Solution:**

| Keys | Description |
|------|-------------|
| `110` `ENTER` | First side's odds, without the minus sign |
| `110` | Second side's odds, without the minus sign |
| `XEQ O` | Runs the program |

**Results (displayed on screen from top to bottom):**

| Register | Value | Meaning |
|----------|-------|---------|
| Z | 4.761905 | 4.76% overround |
| Y | 50.000000 | Fair probability, 50% |
| X | 50.000000 | Fair probability, 50% |

**Interpretation:**

Each side has an implied probability of 52.38%, for a total of 104.76%. With the margin removed, each side has a 50% fair probability.

### 7.3 Profit

**Scenario:**

Find the profit on a 100 stake at −150, and at +130.

**Solution:**

| Keys | Display | Description |
|------|---------|-------------|
| `150` `+/-` `ENTER` `100` `XEQ P` | 66.666667 | Profit at −150 |
| `130` `ENTER` `100` `XEQ P` | 130.000000 | Profit at +130 |

**Interpretation:**

A winning 100 stake at −150 returns 166.67 in total; at +130 it returns 230.00.

### 7.4 Odds Conversion

**Solution:**

| Keys | Display | Description |
|------|---------|-------------|
| `150` `+/-` `XEQ D` | 1.666667 | −150 in decimal odds |
| `130` `XEQ D` | 2.300000 | +130 in decimal odds |
| `2.5` `XEQ A` | 150.000000 | 2.50 in American odds, +150 |
| `1.5` `XEQ A` | -200.000000 | 1.50 in American odds, −200 |

---

## 8. QUICK REFERENCE

### 8.1 Program Labels

| Label | Function |
|-------|----------|
| **O** | No-vig odds and overround |
| **P** | Profit on a winning wager |
| **D** | American to decimal odds |
| **A** | Decimal to American odds |
| **Z** | Equal odds subroutine (internal) |
| **Y** | Negative odds profit subroutine (internal) |
| **B,C** | Conversion subroutines (internal) |

### 8.2 Inputs

| Program | Y-register | X-register |
|---------|------------|------------|
| **O** | Favorite's odds, no sign | Underdog's odds |
| **P** | American odds, with sign | Stake |
| **D** | — | American odds, with sign |
| **A** | — | Decimal odds |

### 8.3 Important Notes

- LBL O takes the favorite's odds without the minus sign; LBL P and LBL D take American odds with their sign
- LBL O is designed for a favorite against an underdog; a market in which both sides carry negative odds (for example −120 and −105) is calculated correctly only when both odds are equal
- When the two odds entered in LBL O are equal, the program assumes both sides carry negative odds; a −105/+105 market therefore cannot be entered as 105 and 105
- The overround V is the total implied probability above 100%; the bookmaker's hold, 1 − 1 ÷ (A + B), is slightly smaller (4.55% at −110/−110)
- LBL P returns the profit only; add the stake for the total return
- LBL P stores the stake in B, replacing the underdog's fair probability from LBL O
- After LBL Z, A holds the implied probability of each side as a fraction (0.523810 at −110), not a percentage
- To chain conversions, use the result on the stack rather than re-keying the rounded display; 1.909091 keyed in returns −109.999989, not −110

---

## 9. PROGRAM LISTING

The complete program listing is provided below. Program steps are shown in standard DM32 RPN format with label-relative line numbers, as displayed on the calculator. The DM32 does not generate checksums.

### LBL O - No-Vig Odds

```
O01  LBL O  No-vig odds. Y: favorite (no sign),
O02  x=y?   X: underdog. Equal odds?
O03  GTO Z  If so, uses equal-odds routine.
O04  STO U  Stores underdog odds U.
O05  R↓
O06  STO F  Stores favorite odds F.
O07  RCL F
O08  100
O09  +
O10  ÷      F ÷ (F + 100).
O11  STO A  Favorite implied probability.
O12  RCL U
O13  100
O14  x<>y
O15  100
O16  +
O17  ÷      100 ÷ (U + 100).
O18  STO B  Underdog implied probability.
O19  RCL A
O20  +      A + B.
O21  STO Y  Stores total implied probability.
O22  100
O23  ×
O24  100
O25  -      (A + B) × 100 − 100.
O26  STO V  Stores overround V, %.
O27  RCL A
O28  RCL Y
O29  ÷
O30  100
O31  ×      A ÷ (A + B) × 100.
O32  STO A  Favorite fair probability, %.
O33  RCL B
O34  RCL Y
O35  ÷
O36  100
O37  ×      B ÷ (A + B) × 100.
O38  STO B  Underdog fair probability, %.
O39  CLx    Clears stack.
O40  ENTER
O41  RCL V  Z-register: overround, %.
O42  RCL A  Y-register: favorite fair %.
O43  RCL B  X-register: underdog fair %.
O44  RTN
```

### LBL Z - Equal Odds Subroutine

```
Z01  LBL Z  Equal-odds routine.
Z02  STO U  Stores odds U.
Z03  RCL U
Z04  100
Z05  +
Z06  ÷      U ÷ (U + 100).
Z07  STO A  Implied probability, each side.
Z08  RCL A
Z09  +      2A.
Z10  100
Z11  ×
Z12  100
Z13  -      2A × 100 − 100.
Z14  STO V  Stores overround V, %.
Z15  CLx    Clears stack.
Z16  ENTER
Z17  RCL V  Z-register: overround, %.
Z18  50     Y-register: 50 %.
Z19  50     X-register: 50 %.
Z20  RTN
```

### LBL P - Profit Calculator

```
P01  LBL P  Profit. Y: American odds, X: stake.
P02  STO B  Stores stake B.
P03  R↓
P04  STO O  Stores odds O.
P05  x<0?   Negative odds?
P06  GTO Y  If so, uses favorite routine.
P07  R↑     Recovers stake.
P08  ×
P09  100
P10  ÷      Stake × O ÷ 100.
P11  STO W  Stores profit W.
P12  CLx    Clears stack.
P13  ENTER
P14  ENTER
P15  ENTER
P16  RCL W  Returns profit in X.
P17  RTN
```

### LBL Y - Negative Odds Profit Subroutine

```
Y01  LBL Y  Profit on negative odds.
Y02  +/-    |O|.
Y03  R↑     Recovers stake.
Y04  x<>y
Y05  ÷
Y06  100
Y07  ×      Stake ÷ |O| × 100.
Y08  STO W  Stores profit W.
Y09  CLx    Clears stack.
Y10  ENTER
Y11  ENTER
Y12  ENTER
Y13  RCL W  Returns profit in X.
Y14  RTN
```

### LBL A - Decimal to American Odds

```
A01  LBL A  Decimal to American odds.
A02  2
A03  x≤y?   Decimal odds ≥ 2?
A04  GTO B  If so, odds are positive.
A05  CLx
A06  R↓     Recovers decimal odds.
A07  1
A08  -      d − 1.
A09  -100
A10  x<>y
A11  ÷      −100 ÷ (d − 1).
A12  RTN    Returns American odds in X.
```

### LBL B - Positive American Odds Subroutine

```
B01  LBL B  Positive American odds.
B02  CLx
B03  R↓     Recovers decimal odds.
B04  1
B05  -      d − 1.
B06  100
B07  ×      (d − 1) × 100.
B08  RTN    Returns American odds in X.
```

### LBL D - American to Decimal Odds

```
D01  LBL D  American to decimal odds.
D02  x≤0?   Negative odds?
D03  GTO C  If so, uses favorite routine.
D04  100
D05  ÷      O ÷ 100.
D06  1
D07  +      O ÷ 100 + 1.
D08  RTN    Returns decimal odds in X.
```

### LBL C - Negative American Odds Subroutine

```
C01  LBL C  Decimal odds, negative O.
C02  1
C03  x<>y
C04  100
C05  x<>y
C06  ÷      100 ÷ O.
C07  -      1 − 100 ÷ O.
C08  RTN    Returns decimal odds in X.
```

---

### By jacober-calc for SwissMicros DM32

> - [SwissMicros Website](https://www.swissmicros.com)
> - [DM32 product page](https://www.swissmicros.com/product/model-dm32)
> - [SwissMicros full products page](https://www.swissmicros.com/products)
> - [DM32 Online User Manual](https://technical.swissmicros.com/dm32/doc/dm32_user_manual.html)
