def generate_report_data():
    capital = 20000.0
    bank = 20000.0
    reactor = 0.0
    shield = 0.0
    
    q1_weeks = 14 # Sept 20 to end of Dec
    q1_weekly_income = 375.0
    
    q2_weeks = 13 # Jan to end of Mar
    q2_weekly_income = 750.0
    
    # Current yields
    yield_bank = 0.0380
    yield_mo = 0.0590
    yield_schd = 0.0325
    yield_abbv = 0.0279
    yield_jnj = 0.0208
    yield_v = 0.0075
    yield_wmt = 0.0087
    
    yield_reactor = (0.4 * yield_mo) + (0.3 * yield_schd) + (0.2 * yield_abbv) + (0.1 * yield_jnj)
    yield_shield = (0.55 * yield_v) + (0.45 * yield_wmt)
    
    timeline = []
    
    # Q1 Simulation (Sep 20 - Dec 20)
    for w in range(1, q1_weeks + 1):
        capital += q1_weekly_income
        
        if bank < 20000:
            bank += q1_weekly_income
        else:
            reactor += q1_weekly_income
            
        bank += bank * (yield_bank / 52)
        reactor += reactor * (yield_reactor / 52)
        
        timeline.append({"Phase": "Q1 (Grind)", "Week": w, "Total_Equity": round(capital,2), "Bank_SGOV": round(bank,2), "Reactor": round(reactor,2), "Shield": round(shield,2)})
        
    # December Protocol (Dec 20-28)
    harvest_to_bank = reactor * 0.10 # 50% of ABBV (which is 20% of Reactor) = 10%
    reactor -= harvest_to_bank
    bank += harvest_to_bank
    
    timeline.append({"Phase": "Dec Protocol", "Week": "Harvest", "Total_Equity": round(capital,2), "Bank_SGOV": round(bank,2), "Reactor": round(reactor,2), "Shield": round(shield,2)})
    
    # Q2 Simulation
    for w in range(1, q2_weeks + 1):
        capital += q2_weekly_income
        
        total = bank + reactor + shield + q2_weekly_income
        
        t_bank = total * 0.75
        t_reactor = total * 0.20
        t_shield = total * 0.05
        
        if t_bank < 20000:
            t_bank = 20000
            rem = total - 20000
            t_reactor = rem * (20/25)
            t_shield = rem * (5/25)
            
        bank = t_bank
        reactor = t_reactor
        shield = t_shield
        
        bank += bank * (yield_bank / 52)
        reactor += reactor * (yield_reactor / 52)
        shield += shield * (yield_shield / 52)
        
        timeline.append({"Phase": "Q2 (Scale)", "Week": w, "Total_Equity": round(total,2), "Bank_SGOV": round(bank,2), "Reactor": round(reactor,2), "Shield": round(shield,2)})
        
    import pandas as pd
    df = pd.DataFrame(timeline)
    return df

df = generate_report_data()
import tabulate
print(df.to_markdown(index=False))