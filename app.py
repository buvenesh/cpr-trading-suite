import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="CPR Breakout Screener", layout="wide", page_icon="📈")

# --- SYMBOL DICTIONARY ---
MARKET_GROUPS = {
    "NIFTY 50": [
        "ADANIENT.NS", "ADANIPORTS.NS", "APOLLOHOSP.NS", "ASIANPAINT.NS", "AXISBANK.NS", 
        "BAJAJ-AUTO.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", "BPCL.NS", "BHARTIARTL.NS", 
        "BRITANNIA.NS", "CIPLA.NS", "COALINDIA.NS", "DIVISLAB.NS", "DRREDDY.NS", 
        "EICHERMOT.NS", "GRASIM.NS", "HCLTECH.NS", "HDFCBANK.NS", "HDFCLIFE.NS", 
        "HEROMOTOCO.NS", "HINDALCO.NS", "HINDUNILVR.NS", "ICICIBANK.NS", "INDUSINDBK.NS", 
        "INFY.NS", "ITC.NS", "JSWSTEEL.NS", "KOTAKBANK.NS", "LT.NS", "LTIM.NS", 
        "M&M.NS", "MARUTI.NS", "NESTLEIND.NS", "NTPC.NS", "ONGC.NS", "POWERGRID.NS", 
        "RELIANCE.NS", "SBILIFE.NS", "SBIN.NS", "SUNPHARMA.NS", "TATACONSUM.NS", 
        "TATAMOTORS.NS", "TATASTEEL.NS", "TCS.NS", "TECHM.NS", "TITAN.NS", "ULTRACEMCO.NS", 
        "UPL.NS", "WIPRO.NS"
    ],
    "NIFTY BANK": [
        "HDFCBANK.NS", "ICICIBANK.NS", "KOTAKBANK.NS", "AXISBANK.NS", "SBIN.NS", 
        "INDUSINDBK.NS", "BANKBARODA.NS", "AUBANK.NS", "FEDERALBNK.NS", "IDFCFIRSTB.NS", 
        "PNB.NS", "BANDHANBNK.NS"
    ],
    "NIFTY F&O": [
        "AARTIIND.NS", "ABB.NS", "ABBOTINDIA.NS", "ABCAPITAL.NS", "ABFRL.NS", "ACC.NS", "ADANIENT.NS", "ADANIPORTS.NS", 
        "ALKEM.NS", "AMBUJACEM.NS", "APOLLOHOSP.NS", "APOLLOTYRE.NS", "ASHOKLEY.NS", "ASIANPAINT.NS", "ASTRAL.NS", "ATUL.NS", 
        "AUBANK.NS", "AUROPHARMA.NS", "AXISBANK.NS", "BAJAJ-AUTO.NS", "BAJAJFINSV.NS", "BAJFINANCE.NS", "BALKRISIND.NS", "BALRAMCHIN.NS", 
        "BANDHANBNK.NS", "BANKBARODA.NS", "BATAINDIA.NS", "BEL.NS", "BERGEPAINT.NS", "BHARATFORG.NS", "BHARTIARTL.NS", "BHEL.NS", 
        "BIOCON.NS", "BOSCHLTD.NS", "BPCL.NS", "BRITANNIA.NS", "BSOFT.NS", "CANBK.NS", "CANFINHOME.NS", "CHAMBLFERT.NS", 
        "CHOLAFIN.NS", "CIPLA.NS", "COALINDIA.NS", "COFORGE.NS", "COLPAL.NS", "CONCOR.NS", "COROMANDEL.NS", "CROMPTON.NS", 
        "CUB.NS", "CUMMINSIND.NS", "DABUR.NS", "DALBHARAT.NS", "DEEPAKNTR.NS", "DIVISLAB.NS", "DIXON.NS", "DLF.NS", 
        "DRREDDY.NS", "EICHERMOT.NS", "ESCORTS.NS", "EXIDEIND.NS", "FEDERALBNK.NS", "GAIL.NS", "GLENMARK.NS", "GMRINFRA.NS", 
        "GNFC.NS", "GODREJCP.NS", "GODREJPROP.NS", "GRANULES.NS", "GRASIM.NS", "GUJGASLTD.NS", "HAL.NS", "HAVELLS.NS", 
        "HCLTECH.NS", "HDFCAMC.NS", "HDFCBANK.NS", "HDFCLIFE.NS", "HEROMOTOCO.NS", "HINDALCO.NS", "HINDCOPPER.NS", "HINDPETRO.NS", 
        "HINDUNILVR.NS", "ICICIBANK.NS", "ICICIGI.NS", "ICICIPRULI.NS", "IDEA.NS", "IDFCFIRSTB.NS", "IEX.NS", "IGL.NS", 
        "INDHOTEL.NS", "INDIACEM.NS", "INDIAMART.NS", "INDIGO.NS", "INDUSINDBK.NS", "INDUSTOWER.NS", "INFY.NS", "IOC.NS", 
        "IPCALAB.NS", "IRCTC.NS", "ITC.NS", "JINDALSTEL.NS", "JKCEMENT.NS", "JSWSTEEL.NS", "JUBLFOOD.NS", "KOTAKBANK.NS", 
        "LALPATHLAB.NS", "LAURUSLABS.NS", "LICHSGFIN.NS", "LT.NS", "LTIM.NS", "LTTS.NS", "LUPIN.NS", "M&M.NS", 
        "M&MFIN.NS", "MANAPPURAM.NS", "MARICO.NS", "MARUTI.NS", "MCDOWELL-N.NS", "MCX.NS", "METROPOLIS.NS", "MFSL.NS", 
        "MGL.NS", "MOTHERSON.NS", "MPHASIS.NS", "MRF.NS", "MUTHOOTFIN.NS", "NATIONALUM.NS", "NAUKRI.NS", "NAVINFLUOR.NS", 
        "NESTLEIND.NS", "NMDC.NS", "NTPC.NS", "OBEROIRLTY.NS", "OFSS.NS", "ONGC.NS", "PAGEIND.NS", "PEL.NS", 
        "PERSISTENT.NS", "PETRONET.NS", "PFC.NS", "PIDILITIND.NS", "PIIND.NS", "PNB.NS", "POLYCAB.NS", "POWERGRID.NS", 
        "PVRINOX.NS", "RAMCOCEM.NS", "RBLBANK.NS", "RECLTD.NS", "RELIANCE.NS", "SAIL.NS", "SBICARD.NS", "SBILIFE.NS", 
        "SBIN.NS", "SHREECEM.NS", "SHRIRAMFIN.NS", "SIEMENS.NS", "SRF.NS", "SUNPHARMA.NS", "SUNTV.NS", "SYNGENE.NS", 
        "TATACHEM.NS", "TATACOMM.NS", "TATACONSUM.NS", "TATAMOTORS.NS", "TATAPOWER.NS", "TATASTEEL.NS", "TCS.NS", "TECHM.NS", 
        "TITAN.NS", "TORNTPHARM.NS", "TRENT.NS", "TVSMOTOR.NS", "UBL.NS", "ULTRACEMCO.NS", "UPL.NS", "VEDL.NS", 
        "VOLTAS.NS", "WIPRO.NS", "ZEEL.NS", "ZYDUSLIFE.NS"
    ],
    "NIFTY Midcap 150": [
        "AARTIIND.NS", "AAVAS.NS", "ABB.NS", "ABCAPITAL.NS", "ABFRL.NS", "ACC.NS", "ADANIENSOL.NS", "ADANIPOWER.NS", 
        "AEGISCHEM.NS", "AFFLE.NS", "AJANTPHARM.NS", "ALKEM.NS", "ALKYLAMINE.NS", "ALOKINDS.NS", "AMARAJABAT.NS", "AMBER.NS", 
        "APLLTD.NS", "APOLLOTYRE.NS", "APTUS.NS", "ASHOKLEY.NS", "ASTERDM.NS", "ASTRAL.NS", "ATUL.NS", "AUBANK.NS", 
        "AUROPHARMA.NS", "AVANTIFEED.NS", "BALAMINES.NS", "BALKRISIND.NS", "BALRAMCHIN.NS", "BANDHANBNK.NS", "BANKBARODA.NS", "BANKINDIA.NS", 
        "BATAINDIA.NS", "BAYERCROP.NS", "BDL.NS", "BEL.NS", "BEML.NS", "BERGEPAINT.NS", "BHARATFORG.NS", "BHEL.NS", 
        "BIOCON.NS", "BIRLACORPN.NS", "BLUESTARCO.NS", "BSOFT.NS", "CAMS.NS", "CANBK.NS", "CANFINHOME.NS", "CARBORUNIV.NS", 
        "CASTROLIND.NS", "CEATLTD.NS", "CENTRALBK.NS", "CENTURYPLY.NS", "CENTURYTEX.NS", "CGPOWER.NS", "CHALET.NS", "CHAMBLFERT.NS", 
        "CHOLAFIN.NS", "CLEAN.NS", "COFORGE.NS", "CONCOR.NS", "COROMANDEL.NS", "CREDITACC.NS", "CROMPTON.NS", "CUB.NS", 
        "CUMMINSIND.NS", "CYIENT.NS", "DALBHARAT.NS", "DATAPATTNS.NS", "DEEPAKNTR.NS", "DELHIVERY.NS", "DEVYANI.NS", "DIXON.NS", 
        "EASEMYTRIP.NS", "ECLERX.NS", "EDELWEISS.NS", "EIHOTEL.NS", "ELGIEQUIP.NS", "EMAMILTD.NS", "ENDURANCE.NS", "ENGINERSIN.NS", 
        "EQUITASBNK.NS", "ERIS.NS", "ESCORTS.NS", "EXIDEIND.NS", "FEDERALBNK.NS", "FINEORG.NS", "FINPIPE.NS", "FORTIS.NS", 
        "FSL.NS", "GAIL.NS", "GICRE.NS", "GLENMARK.NS", "GMRINFRA.NS", "GODREJAGRO.NS", "GODREJCP.NS", "GODREJIND.NS", 
        "GODREJPROP.NS", "GRANULES.NS", "GUJGASLTD.NS", "HAL.NS", "HAPPSTMNDS.NS", "HAVELLS.NS", "HDFCAMC.NS", "HEG.NS", 
        "HFCL.NS", "HINDCOPPER.NS", "HINDPETRO.NS", "HINDZINC.NS", "HUDCO.NS", "ICICIGI.NS", "ICICIPRULI.NS", "IDBI.NS", 
        "IDFC.NS", "IDFCFIRSTB.NS", "IEX.NS", "IGL.NS", "IIFL.NS", "INDHOTEL.NS", "INDIACEM.NS", "INDIAMART.NS", 
        "INDIANB.NS", "INDIGO.NS", "INDUSTOWER.NS", "IPCALAB.NS", "IRB.NS", "IRCON.NS", "IRCTC.NS", "IRFC.NS", 
        "ISEC.NS", "ITI.NS", "J&KBANK.NS", "JBCHEPHARM.NS", "JINDALSTEL.NS", "JKCEMENT.NS", "JKLAKSHMI.NS", "JSWENERGY.NS", 
        "JUBLFOOD.NS", "KALYANKJIL.NS", "KANSAINER.NS", "KARURVYSYA.NS", "KEC.NS", "KEI.NS", "KPITTECH.NS", "KPRMILL.NS", 
        "KRBL.NS", "L&TFH.NS", "LALPATHLAB.NS", "LAURUSLABS.NS", "LICHSGFIN.NS", "LINDEINDIA.NS", "LTTS.NS", "LUPIN.NS", 
        "M&MFIN.NS", "MAHABANK.NS", "MAHSEAMLES.NS", "MANAPPURAM.NS", "MAPMYINDIA.NS", "MARICO.NS", "MAXHEALTH.NS", "MAZDOCK.NS", 
        "MCX.NS", "METROPOLIS.NS", "MFSL.NS", "MGL.NS", "MOTHERSON.NS", "MPHASIS.NS", "MRPL.NS", "MUTHOOTFIN.NS", 
        "NATIONALUM.NS", "NAUKRI.NS", "NAVINFLUOR.NS", "NMDC.NS", "NYKAA.NS", "OBEROIRLTY.NS", "OFSS.NS", "OIL.NS", 
        "PAGEIND.NS", "PATANJALI.NS", "PAYTM.NS", "PEL.NS", "PERSISTENT.NS", "PETRONET.NS", "PFC.NS", "PHOENIXLTD.NS", 
        "PIIND.NS", "PNB.NS", "POLYCAB.NS", "POONAWALLA.NS", "PRAJIND.NS", "PRESTIGE.NS", "PVRINOX.NS", "QUESS.NS", 
        "RADICO.NS", "RAIN.NS", "RAJESHEXPO.NS", "RAMCOCEM.NS", "RATNAMANI.NS", "RAYMOND.NS", "RBLBANK.NS", "RECLTD.NS", 
        "REDINGTON.NS", "RELAXO.NS", "RITES.NS", "RVNL.NS", "SAIL.NS", "SANOFI.NS", "SAPPHIRE.NS", "SBICARD.NS", 
        "SHRIRAMFIN.NS", "SIEMENS.NS", "SJVN.NS", "SKFINDIA.NS", "SOLARINDS.NS", "SONACOMS.NS", "SONATSOFTW.NS", "SPARC.NS", 
        "SRF.NS", "STARHEALTH.NS", "SUMICHEM.NS", "SUNDARMFIN.NS", "SUNDRMFAST.NS", "SUNTV.NS", "SUPREMEIND.NS", "SUZLON.NS", 
        "SYNGENE.NS", "TATACHEM.NS", "TATACOMM.NS", "TATAELXSI.NS", "TATAPOWER.NS", "TORNTPHARM.NS", "TORNTPOWER.NS", "TRENT.NS", 
        "TRIDENT.NS", "TRITURBINE.NS", "TVSMOTOR.NS", "UBL.NS", "UNIONBANK.NS", "UTIAMC.NS", "VARDHMAN.NS", "VBL.NS", 
        "VEDL.NS", "VINATIORGA.NS", "VOLTAS.NS", "WHIRLPOOL.NS", "YESBANK.NS", "ZEEL.NS", "ZOMATO.NS", "ZYDUSLIFE.NS"
    ],
    "NIFTY MidSmallcap 400": [
       "AARTIIND.NS", "AAVAS.NS", "ABB.NS", "ABBOTINDIA.NS", "ABCAPITAL.NS", "ABFRL.NS", "ACC.NS", "ACI.NS", "ADANIENSOL.NS", 
       "ADANIGREEN.NS", "ADANIPOWER.NS", "ADANITRANS.NS", "AEGISCHEM.NS", "AETHER.NS", "AFFLE.NS", "AJANTPHARM.NS", "ALKEM.NS", 
       "ALKYLAMINE.NS", "ALLCARGO.NS", "ALOKINDS.NS", "AMARAJABAT.NS", "AMBER.NS", "AMBUJACEM.NS", "ANANDAMATH.NS", "ANGELONE.NS", 
       "ANURAS.NS", "APARINDS.NS", "APOLLOHOSP.NS", "APOLLOTYRE.NS", "APTUS.NS", "ASAHIINDIA.NS", "ASHOKLEY.NS", "ASIANPAINT.NS", 
       "ASTERDM.NS", "ASTRAL.NS", "ATUL.NS", "AUBANK.NS", "AUROPHARMA.NS", "AVANTIFEED.NS", "AWL.NS", "BAJAJ-AUTO.NS", 
       "BAJAJELEC.NS", "BAJAJFINSV.NS", "BAJAJHLDNG.NS", "BALAMINES.NS", "BALKRISIND.NS", "BALRAMCHIN.NS", "BANDHANBNK.NS", "BANKBARODA.NS", 
       "BANKBOI.NS", "BANKINDIA.NS", "BATAINDIA.NS", "BAYERCROP.NS", "BBDTO.NS", "BDL.NS", "BEL.NS", "BEML.NS", "BERGEPAINT.NS", 
       "BHARATFORG.NS", "BHARTIARTL.NS", "BHEL.NS", "BIOCON.NS", "BIRLACORPN.NS", "BLS.NS", "BLUESTARCO.NS", "BOSCHLTD.NS", 
       "BRIGADE.NS", "BRITANNIA.NS", "BSE.NS", "BSOFT.NS", "CAMS.NS", "CANBK.NS", "CANFINHOME.NS", "CARBORUNIV.NS", 
       "CASTROLIND.NS", "CCL.NS", "CDSL.NS", "CEATLTD.NS", "CENTRALBK.NS", "CENTURYPLY.NS", "CENTURYTEX.NS", "CERA.NS", 
       "CGPOWER.NS", "CHALET.NS", "CHAMBLFERT.NS", "CHEMPLASTS.NS", "CHENNPETRO.NS", "CHOLAFIN.NS", "CIPLA.NS", "CLEAN.NS", 
       "COCHINSHIP.NS", "COFORGE.NS", "COLPAL.NS", "CONCOR.NS", "COROMANDEL.NS", "CRAFTSMAN.NS", "CREDITACC.NS", "CRISIL.NS", 
       "CROMPTON.NS", "CSBBANK.NS", "CUB.NS", "CUMMINSIND.NS", "CYIENT.NS", "DABUR.NS", "DALBHARAT.NS", "DATAPATTNS.NS", 
       "DCMSHRIRAM.NS", "DEEPAKNTR.NS", "DELHIVERY.NS", "DEVYANI.NS", "DIVISLAB.NS", "DIXON.NS", "DLF.NS", "DMART.NS", 
       "DRREDDY.NS", "EASEMYTRIP.NS", "ECLERX.NS", "EICHERMOT.NS", "EIHOTEL.NS", "ELGIEQUIP.NS", "EMAMILTD.NS", "ENDURANCE.NS", 
       "ENGINERSIN.NS", "EPL.NS", "EQUITASBNK.NS", "ERIS.NS", "ESCORTS.NS", "EXIDEIND.NS", "FACT.NS", "FDC.NS", "FEDERALBNK.NS", 
       "FINCABLES.NS", "FINEORG.NS", "FINPIPE.NS", "FSL.NS", "GAIL.NS", "GARFIBRES.NS", "GICRE.NS", "GILLETTE.NS", "GLAND.NS", 
       "GLAXO.NS", "GLENMARK.NS", "GMMPFAUDLR.NS", "GMRINFRA.NS", "GNFC.NS", "GODFRYPHLP.NS", "GODREJAGRO.NS", "GODREJCP.NS", 
       "GODREJIND.NS", "GODREJPROP.NS", "GOCOLORS.NS", "GRANULES.NS", "GRASIM.NS", "GRINDWELL.NS", "GSFC.NS", "GSPL.NS", 
       "GUJALKALI.NS", "GUJGASLTD.NS", "HAL.NS", "HAPPSTMNDS.NS", "HAVELLS.NS", "HCLTECH.NS", "HDFCAMC.NS", "HDFCBANK.NS", 
       "HDFCLIFE.NS", "HEG.NS", "HEROMOTOCO.NS", "HFCL.NS", "HIKAL.NS", "HIL.NS", "HINDALCO.NS", "HINDCOPPER.NS", "HINDPETRO.NS", 
       "HINDUNILVR.NS", "HINDZINC.NS", "HONAUT.NS", "HUDCO.NS", "ICICIBANK.NS", "ICICIGI.NS", "ICICIPRULI.NS", "IDBI.NS", 
       "IDEA.NS", "IDFCFIRSTB.NS", "IEX.NS", "IGL.NS", "IIFL.NS", "INDHOTEL.NS", "INDIACEM.NS", "INDIAMART.NS", "INDIANB.NS", 
       "INDIGO.NS", "INDIGOPNTS.NS", "INDOCO.NS", "INDPETRO.NS", "INDUSINDBK.NS", "INDUSTOWER.NS", "INFIBEAM.NS", "INFY.NS", 
       "INGERRAND.NS", "INTELLECT.NS", "IOC.NS", "IOB.NS", "IPCALAB.NS", "IRB.NS", "IRCON.NS", "IRCTC.NS", "IRFC.NS", 
       "ISEC.NS", "ITC.NS", "ITI.NS", "J&KBANK.NS", "JAMNAAUTO.NS", "JBCHEPHARM.NS", "JINDALSTEL.NS", "JKCEMENT.NS", "JKLAKSHMI.NS", 
       "JKPAPER.NS", "JKTYRE.NS", "JSL.NS", "JSWENERGY.NS", "JSWSTEEL.NS", "JUBLFOOD.NS", "JUBLINGREA.NS", "JUBLPHARMA.NS", 
       "JUSTDIAL.NS", "JYOTHYLAB.NS", "KAJARIACER.NS", "KALPATPOWR.NS", "KALYANKJIL.NS", "KANSAINER.NS", "KARURVYSYA.NS", "KEC.NS", 
       "KEI.NS", "KIMS.NS", "KOTAKBANK.NS", "KPITTECH.NS", "KPRMILL.NS", "KRBL.NS", "L&TFH.NS", "LALPATHLAB.NS", "LATENTVIEW.NS", 
       "LAURUSLABS.NS", "LAXMIMACH.NS", "LEMONTREE.NS", "LICHSGFIN.NS", "LICI.NS", "LINDEINDIA.NS", "LODHA.NS", "LT.NS", 
       "LTIM.NS", "LTTS.NS", "LUPIN.NS", "LUXIND.NS", "M&M.NS", "M&MFIN.NS", "MACROTECH.NS", "MAHABANK.NS", "MAHSEAMLES.NS", 
       "MAHSCOOTER.NS", "MANAPPURAM.NS", "MANYAVAR.NS", "MAPMYINDIA.NS", "MARICO.NS", "MARUTI.NS", "MASTEK.NS", "MAXHEALTH.NS", 
       "MAZDOCK.NS", "MCDOWELL-N.NS", "MCX.NS", "MEDPLUS.NS", "METROBRAND.NS", "METROPOLIS.NS", "MFSL.NS", "MGL.NS", 
       "MHRIL.NS", "MIDHANI.NS", "MINDACORP.NS", "MOTHERSON.NS", "MOTILALOFS.NS", "MPHASIS.NS", "MRF.NS", "MRPL.NS", 
       "MTARTECH.NS", "MUTHOOTFIN.NS", "NATCOPHARM.NS", "NATIONALUM.NS", "NAUKRI.NS", "NAVA.NS", "NAVINFLUOR.NS", "NCC.NS", 
       "NESTLEIND.NS", "NETWORK18.NS", "NH.NS", "NHPC.NS", "NLCINDIA.NS", "NMDC.NS", "NOCIL.NS", "NTPC.NS", "NUVASYS.NS", 
       "NYKAA.NS", "OBEROIRLTY.NS", "OFSS.NS", "OIL.NS", "OLECTRA.NS", "ONGC.NS", "PAGEIND.NS", "PATANJALI.NS", "PAYTM.NS", 
       "PCBL.NS", "PEL.NS", "PERSISTENT.NS", "PETRONET.NS", "PFC.NS", "PFIZER.NS", "PHOENIXLTD.NS", "PIDILITIND.NS", "PIIND.NS", 
       "PNB.NS", "PNBHOUSING.NS", "POLYCAB.NS", "POLYMED.NS", "POONAWALLA.NS", "POWERGRID.NS", "POWERINDIA.NS", "PRAJIND.NS", 
       "PRESTIGE.NS", "PRINCEPIPE.NS", "PRSMJOHNSN.NS", "PTC.NS", "PVRINOX.NS", "QUESS.NS", "RADICO.NS", "RAILTEL.NS", 
       "RAIN.NS", "RAJESHEXPO.NS", "RAMCOCEM.NS", "RATEGAIN.NS", "RATNAMANI.NS", "RAYMOND.NS", "RBA.NS", "RBLBANK.NS", 
       "RECLTD.NS", "REDINGTON.NS", "RELAXO.NS", "RELIANCE.NS", "RENUKA.NS", "RESILITECH.NS", "RITES.NS", "RKFORGE.NS", 
       "ROUTE.NS", "RSYSTEMS.NS", "RUSTOMJEE.NS", "RVNL.NS", "SAFARI.NS", "SAIL.NS", "SANOFI.NS", "SAPPHIRE.NS", "SAREGAMA.NS", 
       "SBICARD.NS", "SBILIFE.NS", "SBIN.NS", "SCHAEFFLER.NS", "SFL.NS", "SHILPAMED.NS", "SHOIPERS.NS", "SHREECEM.NS", 
       "SHRIRAMFIN.NS", "SHYAMMETL.NS", "SIEMENS.NS", "SIS.NS", "SJVN.NS", "SKFINDIA.NS", "SOBHA.NS", "SOLARINDS.NS", 
       "SONACOMS.NS", "SONATSOFTW.NS", "SPARC.NS", "SRF.NS", "STARHEALTH.NS", "STLTECH.NS", "SUMICHEM.NS", "SUNDARMFIN.NS", 
       "SUNDRMFAST.NS", "SUNPHARMA.NS", "SUNTECK.NS", "SUNTV.NS", "SUPRAJIT.NS", "SUPREMEIND.NS", "SUVENPHAR.NS", "SUZLON.NS", 
       "SWANENERGY.NS", "SYMPHONY.NS", "SYNGENE.NS", "TATACHEM.NS", "TATACOMM.NS", "TATACONSUM.NS", "TATAELXSI.NS", 
       "TATAINVEST.NS", "TATAMOTORS.NS", "TATAMTRDVR.NS", "TATAPOWER.NS", "TATASTEEL.NS", "TCS.NS", "TECHM.NS", "TEJASNET.NS", 
       "THERMAX.NS", "TIMKEN.NS", "TITAN.NS", "TORNTPHARM.NS", "TORNTPOWER.NS", "TRENT.NS", "TRIDENT.NS", "TRITURBINE.NS", 
       "TTKPRESTIG.NS", "TTML.NS", "TV18BRDCST.NS", "TVSMOTOR.NS", "UBL.NS", "UCOBANK.NS", "UJJIVANSFB.NS", "ULTRACEMCO.NS", 
       "UNIONBANK.NS", "UPL.NS", "UTIAMC.NS", "VAIBHAVGBL.NS", "VARDHMAN.NS", "VARROC.NS", "VBL.NS", "VEDL.NS", "VENKEYS.NS", 
       "VIJAYA.NS", "VINATIORGA.NS", "VIPIND.NS", "VOLTAS.NS", "VRLLOG.NS", "VSTIND.NS", "WABAG.NS", "WELCORP.NS", 
       "WELENT.NS", "WELSPUNIND.NS", "WESTLIFE.NS", "WHIRLPOOL.NS", "WIPRO.NS", "YESBANK.NS", "ZEEL.NS", "ZENSARTECH.NS", 
       "ZFCVINDIA.NS", "ZOMATO.NS", "ZYDUSLIFE.NS", "ZYDUSWELL.NS"
   ]
}

# --- PIVOT BOSS THRESHOLDS ---
V_NARROW_MAX = 5.0
NARROW_MAX = 15.0
MID_MAX = 30.0

st.title("📈 Advanced CPR Trading Suite")

tab1, tab2 = st.tabs(["📊 Stock Breakout Screener", "🎯 Auto Index CPR Tracker"])

# ==========================================
# TAB 1: STOCK SCREENER
# ==========================================
with tab1:
    st.markdown("Scan stocks for breakouts and narrow CPRs.")
    c1, c2, c3, c4 = st.columns(4)
    with c1: target_date = st.date_input("Target Date", datetime.date.today() - datetime.timedelta(days=1), key="t1_d")
    with c2: selected_group = st.selectbox("Select Index Group", list(MARKET_GROUPS.keys()))
    with c3: pivot_gap_prc = st.number_input("Pivot Gap %", value=0.05, step=0.01) / 100
    with c4: st.markdown("<br>", unsafe_allow_html=True); run_btn = st.button("🚀 Run Analysis")

    if run_btn:
        symbols = MARKET_GROUPS[selected_group]
        html_rows = ""
        status_text = st.empty(); my_bar = st.progress(0)
        for idx, sym in enumerate(symbols):
            clean_sym = sym.replace('.NS', '')
            status_text.text(f"Analyzing {clean_sym} ({idx+1}/{len(symbols)})...")
            my_bar.progress((idx + 1) / len(symbols))
            try:
                ticker = yf.Ticker(sym); df = ticker.history(period="2mo")
                df.index = df.index.tz_localize(None).date
                if target_date not in df.index: continue
                t_idx = df.index.get_loc(target_date)
                today = df.iloc[t_idx]
                t_o, t_h, t_l, t_c = today['Open'], today['High'], today['Low'], today['Close']
                t_v = float(today['Volume'])
                p4h = float(df['High'].iloc[t_idx-4 : t_idx].max())
                av = float(df['Volume'].iloc[t_idx-10 : t_idx].mean())
                c_txt, c_cls = ("Red Candle", "bg-red") if t_c < t_o else ("Green Candle", "bg-green") if t_c > t_o else ("Doji", "bg-yellow")
                v_txt, v_cls = ("Good", "bg-green") if t_v > (av*2) else ("Average", "bg-yellow") if t_v > av else ("Low", "bg-red")
                p = (t_h+t_l+t_c)/3; b = (t_h+t_l)/2; t = (p-b)+p
                is_n = "Yes" if abs(t-b) <= (pivot_gap_prc*t_c) else "No"; n_cls = "bg-green" if is_n == "Yes" else ""
                if t_c <= t_o or t_c <= p4h: bo_txt, bo_cls = "No Breakout", "bg-red"
                elif (t_h-t_o) >= (5*(t_h-t_c)): bo_txt, bo_cls = "Breakout", "bg-green"
                else: bo_txt, bo_cls = "Big Sell Wick", "bg-yellow"
                html_rows += f"<tr><td><strong>{clean_sym}</strong></td><td>{t_o:.2f}</td><td>{t_h:.2f}</td><td>{t_l:.2f}</td><td>{t_c:.2f}</td><td>{p4h:.2f}</td><td>{int(t_v)}</td><td class='{c_cls}'>{c_txt}</td><td class='{v_cls}'>{v_txt}</td><td class='{n_cls}'>{is_n}</td><td class='{bo_cls}'>{bo_txt}</td><td><a href='https://gocharting.com/terminal?ticker=NSE:{clean_sym}&layout=1' target='_blank'>Chart</a></td></tr>"
            except: pass
        my_bar.empty(); status_text.empty()
        if html_rows:
            st.components.v1.html(f"<style>table {{ width: 100%; border-collapse: collapse; background: #1e1e1e; font-family: sans-serif; font-size: 14px; color: #e0e0e0; }} th, td {{ padding: 10px; border: 1px solid #333; text-align: center; }} th {{ background-color: #2d2d2d; cursor: pointer; }} .bg-red {{ color: #ff6b6b; font-weight: bold;}} .bg-green {{ color: #6bff6b; font-weight: bold;}} .bg-yellow {{ color: #ffff6b; font-weight: bold;}}</style><table><thead><tr><th>Symbol</th><th>Open</th><th>High</th><th>Low</th><th>Close</th><th>Prev 4D High</th><th>Volume</th><th>Candle</th><th>Vol Status</th><th>Narrow CPR</th><th>Breakout Status</th><th>Chart</th></tr></thead><tbody>{html_rows}</tbody></table>", height=800, scrolling=True)
        else: st.error("No data found.")

# ==========================================
# TAB 2: INDEX CPR TRACKER
# ==========================================
with tab2:
    st.markdown("### 🎯 Tomorrow's Index CPR Outlook")
    # Date Selector for Index Data
    idx_date = st.date_input("Select Base Data Date", datetime.date.today() - datetime.timedelta(days=1), key="idx_date_sel")
    st.markdown("---")

    indices = {"NIFTY 50": "^NSEI", "NIFTY BANK": "^NSEBANK"}
    
    # We remove the columns here and display them sequentially to avoid "nested columns" errors
    for idx_name, sym in indices.items():
        st.subheader(idx_name)
        try:
            ticker = yf.Ticker(sym); df = ticker.history(period="3mo")
            df.index = df.index.tz_localize(None).date
            
            if idx_date in df.index:
                # Calculate ADR (Average Daily Range)
                df['Range'] = df['High'] - df['Low']
                curr_idx = df.index.get_loc(idx_date)
                if curr_idx < 14:
                    st.warning(f"Not enough historical data before {idx_date} to calculate ADR.")
                    continue
                
                adr = df['Range'].iloc[curr_idx-13 : curr_idx+1].mean()
                row = df.iloc[curr_idx]
                h, l, c = float(row['High']), float(row['Low']), float(row['Close'])
                
                p = (h+l+c)/3; b = (h+l)/2; t = (p-b)+p
                if b > t: t, b = b, t
                w_pts = t-b
                w_prc = (w_pts / adr) * 100
                
                # Display Metrics in a cleaner way without nesting
                st.write(f"**Data Date:** {idx_date} | **Tomorrow's Pivot:** ₹{p:,.2f}")
                st.write(f"**TCP:** ₹{t:,.2f} | **BCP:** ₹{b:,.2f} | **Close:** ₹{c:,.2f}")
                
                if w_prc < V_NARROW_MAX:
                    st.success(f"🟢 **Very Narrow CPR** ({w_prc:.1f}% of ADR) | Expectation: Strong Trending")
                elif w_prc <= NARROW_MAX:
                    st.info(f"🔵 **Narrow CPR** ({w_prc:.1f}% of ADR) | Expectation: Trending Day")
                elif w_prc <= MID_MAX:
                    st.warning(f"🟠 **Average CPR** ({w_prc:.1f}% of ADR) | Expectation: Normal Day")
                else:
                    st.error(f"🔴 **Wide CPR** ({w_prc:.1f}% of ADR) | Expectation: Sideways")
            else:
                st.error(f"Market was closed on {idx_date}. Please select a trading day.")
        except Exception as e:
            st.error(f"Error fetching {idx_name}: {e}")
        st.markdown("---")