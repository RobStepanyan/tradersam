# Generated by Django 3.0.5 on 2020-05-03 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_app', '0127_auto_20200429_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='australiaetfstaticinfo',
            name='issuer',
            field=models.CharField(choices=[('Switzer Asset Management Limited', 'Switzer Asset Management Limited'), ('Russell Investment Management Limited', 'Russell Investment Management Limited'), ('InvestSMART Funds Management Ltd', 'InvestSMART Funds Management Ltd'), ('Magellan Asset Management Limited', 'Magellan Asset Management Limited'), ('ETFS', 'ETFS'), ('Platinum Investment Management Ltd', 'Platinum Investment Management Ltd'), ('Russell', 'Russell'), ('Vanguard Investments Australia Ltd', 'Vanguard Investments Australia Ltd'), ('WCM Investment Management', 'WCM Investment Management'), ('SPDR', 'SPDR'), ('iShares', 'iShares'), ('Perennial Investment Management Ltd', 'Perennial Investment Management Ltd'), ('ETFS Management (AUS) Ltd', 'ETFS Management (AUS) Ltd'), ('ETFS Metal Securities Australia Ltd', 'ETFS Metal Securities Australia Ltd'), ('Other', 'Other'), ('The Perth Mint', 'The Perth Mint'), ('Fidelity (FIL Fund Management Limited)', 'Fidelity (FIL Fund Management Limited)'), ('Antipodes Partners Limited', 'Antipodes Partners Limited'), ('K2 Asset Management Ltd', 'K2 Asset Management Ltd'), ('VanEck Investments Limited', 'VanEck Investments Limited'), ('Horizons', 'Horizons'), ('BetaShares Capital Ltd', 'BetaShares Capital Ltd'), ('Montgomery Investment Mgmt Pty Ltd', 'Montgomery Investment Mgmt Pty Ltd'), ('Vanguard', 'Vanguard'), ('VanEck', 'VanEck'), ('ANZ', 'ANZ'), ('UBS AU', 'UBS AU')], max_length=100),
        ),
        migrations.AlterField(
            model_name='australiafundstaticinfo',
            name='issuer',
            field=models.CharField(choices=[('AustralianSuper Pty Ltd', 'AustralianSuper Pty Ltd'), ('Investors Mutual Limited', 'Investors Mutual Limited'), ('DFA Australia Limited', 'DFA Australia Limited'), ('Vanguard', 'Vanguard'), ('Antipodes Partners Limited', 'Antipodes Partners Limited'), ('Russell Investment Management Limited', 'Russell Investment Management Limited'), ('PIMCO Australia Pty Limited', 'PIMCO Australia Pty Limited'), ('Bennelong Funds Management Ltd', 'Bennelong Funds Management Ltd'), ('Challenger Ltd', 'Challenger Ltd'), ('Macquarie Bank Group', 'Macquarie Bank Group'), ('State Street Global Advisors (Aus) Ltd', 'State Street Global Advisors (Aus) Ltd'), ('Vanguard Investments Australia Ltd', 'Vanguard Investments Australia Ltd'), ('T. Rowe Price International Limited', 'T. Rowe Price International Limited'), ('VicSuper Pty Ltd', 'VicSuper Pty Ltd'), ('Electricity Supply Industry Super (Qld)', 'Electricity Supply Industry Super (Qld)'), ('Paradice Investment Management Pty Ltd', 'Paradice Investment Management Pty Ltd'), ('Commonwealth/Colonial Group', 'Commonwealth/Colonial Group'), ('AMP Group', 'AMP Group'), ('Janus Henderson Group PLC', 'Janus Henderson Group PLC'), ('Ellerston Capital Limited', 'Ellerston Capital Limited'), ('Magellan Asset Management Limited', 'Magellan Asset Management Limited'), ('FIL Australia', 'FIL Australia'), ('Retail Employees Superannuation Pty Ltd', 'Retail Employees Superannuation Pty Ltd'), ('National/MLC Group', 'National/MLC Group'), ('Sunsuper Pty Ltd', 'Sunsuper Pty Ltd'), ('IOOF Group', 'IOOF Group')], max_length=100),
        ),
        migrations.AlterField(
            model_name='canadaetfstaticinfo',
            name='issuer',
            field=models.CharField(choices=[('Franklin Templeton Investments', 'Franklin Templeton Investments'), ('Pimco', 'Pimco'), ('AGF Investments Inc.', 'AGF Investments Inc.'), ('First Asset', 'First Asset'), ('BlackRock', 'BlackRock'), ('National Bank Investments Inc', 'National Bank Investments Inc'), ('PowerShares', 'PowerShares'), ('Horizons ETFs Management (Canada) Inc', 'Horizons ETFs Management (Canada) Inc'), ('Fidelity Investments Canada ULC', 'Fidelity Investments Canada ULC'), ('Auspice Capital Advisors', 'Auspice Capital Advisors'), ('TD AM', 'TD AM'), ('RBC Global Asset Management Inc.', 'RBC Global Asset Management Inc.'), ('Sphere Investment Management Inc', 'Sphere Investment Management Inc'), ('Accelerate Financial Tech Inc', 'Accelerate Financial Tech Inc'), ('Brompton Funds', 'Brompton Funds'), ('Lysander Funds Ltd.', 'Lysander Funds Ltd.'), ('Franklin Templeton Investments Corp', 'Franklin Templeton Investments Corp'), ('iShares', 'iShares'), ('Franklin Templeton', 'Franklin Templeton'), ('Other', 'Other'), ('WisdomTree', 'WisdomTree'), ('Invesco Canada Ltd.', 'Invesco Canada Ltd.'), ('Emerge Canada Inc.', 'Emerge Canada Inc.'), ('Evolve Funds Group Inc.', 'Evolve Funds Group Inc.'), ('Questrade', 'Questrade'), ('Harvest Portfolios Group Inc.', 'Harvest Portfolios Group Inc.'), ('SmartBe Wealth Inc', 'SmartBe Wealth Inc'), ('Purpose', 'Purpose'), ('TD Asset Management', 'TD Asset Management'), ('Mackenzie', 'Mackenzie'), ('CIBC Asset Management Inc', 'CIBC Asset Management Inc'), ('RBS', 'RBS'), ('Manulife Investments', 'Manulife Investments'), ('Purpose Investments Inc.', 'Purpose Investments Inc.'), ('Harvest', 'Harvest'), ('Starlight Investments Capital LP', 'Starlight Investments Capital LP'), ('Sprott', 'Sprott'), ('Vanguard Investments Canada Inc', 'Vanguard Investments Canada Inc'), ('First Trust', 'First Trust'), ('Fidelity', 'Fidelity'), ('Desjardins Global Asset Management', 'Desjardins Global Asset Management'), ('BMO', 'BMO'), ('Horizons', 'Horizons'), ('RBC Global', 'RBC Global'), ('BMO Asset Management Inc', 'BMO Asset Management Inc'), ('BlackRock Asset Management Canada Ltd', 'BlackRock Asset Management Canada Ltd'), ('First Asset Investment Management Inc', 'First Asset Investment Management Inc'), ('QuantShares', 'QuantShares'), ('Vanguard', 'Vanguard'), ('Picton Mahoney Asset Management', 'Picton Mahoney Asset Management'), ('PIMCO Canada', 'PIMCO Canada'), ('Bristol Gate Capital Partners', 'Bristol Gate Capital Partners'), ('Hamilton Capital Partners Inc.', 'Hamilton Capital Partners Inc.')], max_length=100),
        ),
        migrations.AlterField(
            model_name='canadafundstaticinfo',
            name='issuer',
            field=models.CharField(choices=[('EdgePoint Wealth Management Inc', 'EdgePoint Wealth Management Inc'), ('Capital International Asset Mngmt', 'Capital International Asset Mngmt'), ('Investors Group Inc', 'Investors Group Inc'), ('TD Asset Management Inc', 'TD Asset Management Inc'), ('Desjardins Investments Inc', 'Desjardins Investments Inc'), ('Manulife Investments', 'Manulife Investments'), ('Scotia Asset Management', 'Scotia Asset Management'), ('PIMCO Canada', 'PIMCO Canada'), ('Beutel, Goodman & Company Ltd.', 'Beutel, Goodman & Company Ltd.'), ('RBC Global Asset Management Inc.', 'RBC Global Asset Management Inc.'), ('Fidelity Investments Canada ULC', 'Fidelity Investments Canada ULC')], max_length=100),
        ),
        migrations.AlterField(
            model_name='chinaetfstaticinfo',
            name='issuer',
            field=models.CharField(choices=[('Lion Fund Mgmt Co.,Ltd', 'Lion Fund Mgmt Co.,Ltd'), ('Harvest Fund Mgmt Co.,Ltd', 'Harvest Fund Mgmt Co.,Ltd'), ('CCB Principal Asset Mgmt Co.,Ltd', 'CCB Principal Asset Mgmt Co.,Ltd'), ('China Southern Fund Mgmt Co.,Ltd', 'China Southern Fund Mgmt Co.,Ltd'), ('E Fund', 'E Fund'), ('Nanhua', 'Nanhua'), ('China Asset Management Co., Ltd.', 'China Asset Management Co., Ltd.'), ('Fubon', 'Fubon'), ('Bosera', 'Bosera'), ('China Life AMP Asset Management Co.Ltd', 'China Life AMP Asset Management Co.Ltd'), ('Fortune SG', 'Fortune SG'), ('GuoTai', 'GuoTai'), ('Fortune SG Fund Management CO.,Ltd', 'Fortune SG Fund Management CO.,Ltd'), ('China Southern', 'China Southern'), ('Golden Eagle Asset Management Co.,Ltd', 'Golden Eagle Asset Management Co.,Ltd'), ('AXA SPDB Investment Managers Co.,Ltd', 'AXA SPDB Investment Managers Co.,Ltd'), ('ICBC Credit Suisse Asset Mgmt Co.,Ltd', 'ICBC Credit Suisse Asset Mgmt Co.,Ltd'), ('CIB Fund Management Co.,Ltd', 'CIB Fund Management Co.,Ltd'), ('Fullgoal Fund Mgmt Co.,Ltd', 'Fullgoal Fund Mgmt Co.,Ltd'), ('GF Fund Mgmt Co.,Ltd', 'GF Fund Mgmt Co.,Ltd'), ('HuaAn Fund Mgmt Co., Ltd', 'HuaAn Fund Mgmt Co., Ltd'), ('China Universal Asset Mgmt Co.Ltd', 'China Universal Asset Mgmt Co.Ltd'), ('Other', 'Other'), ('New China Fund Mgmt Co.,Ltd', 'New China Fund Mgmt Co.,Ltd'), ('Hwabao WP Fund Management Co.,Ltd', 'Hwabao WP Fund Management Co.,Ltd'), ('HuaAn', 'HuaAn'), ('HFT Investment Mgmt Co., Ltd', 'HFT Investment Mgmt Co., Ltd'), ('Invesco Great Wall Fund Mgmt Co. Ltd', 'Invesco Great Wall Fund Mgmt Co. Ltd'), ('China Merchants Fund Mgmt Co.,Ltd', 'China Merchants Fund Mgmt Co.,Ltd'), ('DaCheng', 'DaCheng'), ('Guotai Asset Mgmt Co.,Ltd', 'Guotai Asset Mgmt Co.,Ltd'), ('Founder & Fubon Fund Mngmt Co., Ltd.', 'Founder & Fubon Fund Mngmt Co., Ltd.'), ('E Fund Mgmt Co.,Ltd', 'E Fund Mgmt Co.,Ltd'), ('Ping An Fund Management Company Limited', 'Ping An Fund Management Company Limited'), ('Huatai-PB', 'Huatai-PB'), ('SWS MU Fund Management Co., Ltd', 'SWS MU Fund Management Co., Ltd'), ('Ping An of China Asset Management (HK)Co', 'Ping An of China Asset Management (HK)Co'), ('China Asset Mgmt Co.,Ltd', 'China Asset Mgmt Co.,Ltd'), ('Yinhua Fund Mgmt Co., Ltd', 'Yinhua Fund Mgmt Co., Ltd'), ('Penghua Fund Mgmt Co.,Ltd', 'Penghua Fund Mgmt Co.,Ltd'), ('Wanjia Asset Mgmt Co., Ltd', 'Wanjia Asset Mgmt Co., Ltd'), ('China Fund Management Co. Ltd.', 'China Fund Management Co. Ltd.'), ('Bank of Communications Schroders', 'Bank of Communications Schroders'), ('Harvest', 'Harvest'), ('GTJA-Allianz Fund Mgmt Co.,Ltd', 'GTJA-Allianz Fund Mgmt Co.,Ltd'), ('Huatai-PineBridge Fund Mgmt Co., Ltd', 'Huatai-PineBridge Fund Mgmt Co., Ltd'), ('ChinaAMC', 'ChinaAMC'), ('Horizons', 'Horizons'), ('Ping An UOB Fund Management Company Ltd', 'Ping An UOB Fund Management Company Ltd'), ('Bank of China Investment Mgmt Co.,Ltd', 'Bank of China Investment Mgmt Co.,Ltd'), ('Hony Horizon Fund Management Co.,ltd', 'Hony Horizon Fund Management Co.,ltd')], max_length=100),
        ),
        migrations.AlterField(
            model_name='chinafundstaticinfo',
            name='issuer',
            field=models.CharField(choices=[('Harvest Fund Mgmt Co.,Ltd', 'Harvest Fund Mgmt Co.,Ltd'), ('Great Wall Fund Mgmt Co.,Ltd', 'Great Wall Fund Mgmt Co.,Ltd'), ('Yinhua Fund Mgmt Co., Ltd', 'Yinhua Fund Mgmt Co., Ltd'), ('China Merchants Fund Mgmt Co.,Ltd', 'China Merchants Fund Mgmt Co.,Ltd'), ('Invesco Great Wall Fund Mgmt Co. Ltd', 'Invesco Great Wall Fund Mgmt Co. Ltd'), ('BOC International China Ltd', 'BOC International China Ltd'), ('ABC-CA Fund Mgmt Co.,Ltd', 'ABC-CA Fund Mgmt Co.,Ltd'), ('Bank of China Investment Mgmt Co.,Ltd', 'Bank of China Investment Mgmt Co.,Ltd'), ('ICBC Credit Suisse Asset Mgmt Co.,Ltd', 'ICBC Credit Suisse Asset Mgmt Co.,Ltd'), ('CCB Principal Asset Mgmt Co.,Ltd', 'CCB Principal Asset Mgmt Co.,Ltd'), ('Ping An Fund Management Company Limited', 'Ping An Fund Management Company Limited'), ('HuaAn Fund Mgmt Co., Ltd', 'HuaAn Fund Mgmt Co., Ltd'), ('China Southern Fund Mgmt Co.,Ltd', 'China Southern Fund Mgmt Co.,Ltd'), ('China Asset Mgmt Co.,Ltd', 'China Asset Mgmt Co.,Ltd'), ('CIB Fund Management Co.,Ltd', 'CIB Fund Management Co.,Ltd'), ('GF Fund Mgmt Co.,Ltd', 'GF Fund Mgmt Co.,Ltd'), ('Tian Hong Asset Mgmt Co.,Ltd', 'Tian Hong Asset Mgmt Co.,Ltd'), ('Bank of Communications Schroders', 'Bank of Communications Schroders'), ('Rongtong Fund Mgmt Co.,Ltd', 'Rongtong Fund Mgmt Co.,Ltd'), ('ZhongRong Fund Management Co.,Ltd', 'ZhongRong Fund Management Co.,Ltd'), ('Bosera Asset Management Co., Limited', 'Bosera Asset Management Co., Limited'), ('E Fund Mgmt Co.,Ltd', 'E Fund Mgmt Co.,Ltd'), ('AXA SPDB Investment Managers Co.,Ltd', 'AXA SPDB Investment Managers Co.,Ltd'), ('Hwabao WP Fund Management Co.,Ltd', 'Hwabao WP Fund Management Co.,Ltd'), ('Penghua Fund Mgmt Co.,Ltd', 'Penghua Fund Mgmt Co.,Ltd'), ('Lion Fund Mgmt Co.,Ltd', 'Lion Fund Mgmt Co.,Ltd'), ('China International Fund Mgmt Co.,Ltd', 'China International Fund Mgmt Co.,Ltd'), ('China Universal Asset Mgmt Co.Ltd', 'China Universal Asset Mgmt Co.Ltd'), ('Fullgoal Fund Mgmt Co.,Ltd', 'Fullgoal Fund Mgmt Co.,Ltd'), ('AEGON-Industrial Fund Mgmt Co.,Ltd', 'AEGON-Industrial Fund Mgmt Co.,Ltd'), ('UBS SDIC Fund Mgmt Co.,Ltd', 'UBS SDIC Fund Mgmt Co.,Ltd'), ('Lombarda China Fund Mgmt Co.,Ltd', 'Lombarda China Fund Mgmt Co.,Ltd')], max_length=100),
        ),
        migrations.AlterField(
            model_name='germanyetfstaticinfo',
            name='issuer',
            field=models.CharField(choices=[('Pimco', 'Pimco'), ('OSSIAM', 'OSSIAM'), ('DB ETC', 'DB ETC'), ('Deka Investment GmbH', 'Deka Investment GmbH'), ('Deutsche Börse Commodities GmbH', 'Deutsche Börse Commodities GmbH'), ('Lyxor', 'Lyxor'), ('UBS', 'UBS'), ('BlackRock', 'BlackRock'), ('ETFS', 'ETFS'), ('Boost', 'Boost'), ('PowerShares', 'PowerShares'), ('Source', 'Source'), ('HBSC', 'HBSC'), ('ComStage', 'ComStage'), ('SPDR', 'SPDR'), ('iShares', 'iShares'), ('Other', 'Other'), ('THEAM', 'THEAM'), ('WisdomTree', 'WisdomTree'), ('BlackRock Asset Management Ireland - ETF', 'BlackRock Asset Management Ireland - ETF'), ('Amundi', 'Amundi'), ('Deka', 'Deka'), ('Invesco Investment Management Limited', 'Invesco Investment Management Limited'), ('RBS', 'RBS'), ('UBS UK', 'UBS UK'), ('db X-trackers', 'db X-trackers'), ('Lyxor Funds Solutions S.A.', 'Lyxor Funds Solutions S.A.'), ('State Street Global Advisors', 'State Street Global Advisors')], max_length=100),
        ),
        migrations.AlterField(
            model_name='germanyfundstaticinfo',
            name='issuer',
            field=models.CharField(choices=[('DWS Investment GmbH', 'DWS Investment GmbH'), ('Amundi Deutschland GmbH', 'Amundi Deutschland GmbH'), ('FRANKFURT-TRUST Investment-GmbH', 'FRANKFURT-TRUST Investment-GmbH'), ('DWS Investment S.A.', 'DWS Investment S.A.'), ('Landesbank Berlin Investment GmbH', 'Landesbank Berlin Investment GmbH'), ('UBS Fund Management (Luxembourg) S.A.', 'UBS Fund Management (Luxembourg) S.A.'), ('Deka Vermögensmanagement GmbH', 'Deka Vermögensmanagement GmbH'), ('Union Investment Real Estate GmbH', 'Union Investment Real Estate GmbH'), ('RREEF Investment GmbH', 'RREEF Investment GmbH'), ('Savills Fund Management GmbH', 'Savills Fund Management GmbH'), ('AXA Investment Managers Deutschland GmbH', 'AXA Investment Managers Deutschland GmbH'), ('Commerz Real Investment GmbH', 'Commerz Real Investment GmbH'), ('Deka Investment GmbH', 'Deka Investment GmbH'), ('Axxion S.A.', 'Axxion S.A.'), ('Universal-Investment GmbH', 'Universal-Investment GmbH'), ('Comgest Asset Management Intl Ltd', 'Comgest Asset Management Intl Ltd'), ('Westlnvest GmbH', 'Westlnvest GmbH'), ('Union Investment Privatfonds GmbH', 'Union Investment Privatfonds GmbH'), ('DWS Grundbesitz GmbH', 'DWS Grundbesitz GmbH'), ('Wellington Management Company LLP', 'Wellington Management Company LLP'), ('Deutsche Asset Management Investment GmbH', 'Deutsche Asset Management Investment GmbH'), ('Allianz Global Investors GmbH', 'Allianz Global Investors GmbH'), ('M&G Securities Ltd', 'M&G Securities Ltd'), ('Deka Immobilien Investment GmbH', 'Deka Immobilien Investment GmbH')], max_length=100),
        ),
        migrations.AlterField(
            model_name='hketfstaticinfo',
            name='issuer',
            field=models.CharField(choices=[('Samsung', 'Samsung'), ('China International Capital Corporation', 'China International Capital Corporation'), ('E Fund', 'E Fund'), ('Premia Partners Company Limited', 'Premia Partners Company Limited'), ('Bosera', 'Bosera'), ('State Street Global Advisors Asia Ltd', 'State Street Global Advisors Asia Ltd'), ('Hai Tong', 'Hai Tong'), ('ComStage', 'ComStage'), ('E Fund Management (HK) Co., Ltd', 'E Fund Management (HK) Co., Ltd'), ('China Asset Management (HK) Limited', 'China Asset Management (HK) Limited'), ('SPDR', 'SPDR'), ('Yuanta', 'Yuanta'), ('HSBC Investment Funds (HK) Limited', 'HSBC Investment Funds (HK) Limited'), ('iShares', 'iShares'), ('China Intl Capital Corp HK Asse Mgt Ltd.', 'China Intl Capital Corp HK Asse Mgt Ltd.'), ('Value', 'Value'), ('Samsung asset management (HK) Co., Ltd.', 'Samsung asset management (HK) Co., Ltd.'), ('W.I.S.E', 'W.I.S.E'), ('Other', 'Other'), ('Amundi', 'Amundi'), ('Harvest', 'Harvest'), ('CSOP', 'CSOP'), ('ChinaAMC', 'ChinaAMC'), ('Horizons', 'Horizons'), ('Mirae Asset Global Investments (HK) Ltd', 'Mirae Asset Global Investments (HK) Ltd'), ('CSOP Asset Management Limited', 'CSOP Asset Management Limited'), ('BMO', 'BMO'), ('Hang Seng', 'Hang Seng'), ('db X-trackers', 'db X-trackers'), ('Vanguard', 'Vanguard'), ('Mirae Asset', 'Mirae Asset'), ('Lippo Investments Management Limited', 'Lippo Investments Management Limited'), ('State Street Global Advisors', 'State Street Global Advisors')], max_length=100),
        ),
        migrations.AlterField(
            model_name='hkfundstaticinfo',
            name='issuer',
            field=models.CharField(choices=[('BEA Union Investment Management Ltd', 'BEA Union Investment Management Ltd'), ('HSBC Investment Funds (Luxembourg) S.A.', 'HSBC Investment Funds (Luxembourg) S.A.'), ('PineBridge Investments Hong Kong Limited', 'PineBridge Investments Hong Kong Limited'), ('Fidelity (FIL Inv Mgmt (Lux) S.A.)', 'Fidelity (FIL Inv Mgmt (Lux) S.A.)'), ('HSBC Investment Funds (HK) Limited', 'HSBC Investment Funds (HK) Limited'), ('AIA Company (Trustee) Limited', 'AIA Company (Trustee) Limited'), ('Manulife Asset Management (HK) Ltd', 'Manulife Asset Management (HK) Ltd'), ('UBS Fund Management (Luxembourg) S.A.', 'UBS Fund Management (Luxembourg) S.A.'), ('BlackRock (Luxembourg) SA', 'BlackRock (Luxembourg) SA'), ('Sun Life Hong Kong Limited', 'Sun Life Hong Kong Limited'), ('Schroder Investment Management (HK) Ltd', 'Schroder Investment Management (HK) Ltd'), ('BOCI-Prudential Trustee Limited', 'BOCI-Prudential Trustee Limited'), ('Hang Seng Investment Management Ltd', 'Hang Seng Investment Management Ltd'), ('Invesco Hong Kong Limited', 'Invesco Hong Kong Limited'), ('Franklin Templeton Investment Funds', 'Franklin Templeton Investment Funds'), ('JPMorgan Asset Management (Europe) S.à r.l.', 'JPMorgan Asset Management (Europe) S.à r.l.'), ('Pictet Asset Management (Europe) SA', 'Pictet Asset Management (Europe) SA'), ('FIL Investment Management (HK) Ltd', 'FIL Investment Management (HK) Ltd'), ('JPMorgan Funds (Asia) Limited', 'JPMorgan Funds (Asia) Limited'), ('Schroder Investment Management Lux S.A.', 'Schroder Investment Management Lux S.A.'), ('Janus Henderson Investors', 'Janus Henderson Investors'), ('Franklin Templeton International Services S.à r.l.', 'Franklin Templeton International Services S.à r.l.'), ('BOCI-Prudential Asset Management', 'BOCI-Prudential Asset Management'), ('PIMCO Global Advisors (Ireland) Limited', 'PIMCO Global Advisors (Ireland) Limited'), ('AllianceBernstein (Luxembourg) S.à r.l.', 'AllianceBernstein (Luxembourg) S.à r.l.'), ('BlackRock Asset Management North Asia Ltd', 'BlackRock Asset Management North Asia Ltd'), ('HSBC Life (International) Limited', 'HSBC Life (International) Limited'), ('RCM Asia Pacific Limited', 'RCM Asia Pacific Limited'), ('Bank Consortium', 'Bank Consortium'), ('Allianz Global Investors GmbH', 'Allianz Global Investors GmbH'), ('Zeal Asset Management Limited', 'Zeal Asset Management Limited'), ('Principal Trust Company (Asia) Limited', 'Principal Trust Company (Asia) Limited'), ('Value Partners Hong Kong Limited', 'Value Partners Hong Kong Limited')], max_length=100),
        ),
        migrations.AlterField(
            model_name='japanetfstaticinfo',
            name='issuer',
            field=models.CharField(choices=[('Samsung', 'Samsung'), ('Nikko', 'Nikko'), ('UBS', 'UBS'), ('Norinchukin Zenkyoren Asset Mgmt Co.,Ltd', 'Norinchukin Zenkyoren Asset Mgmt Co.,Ltd'), ('Simplex', 'Simplex'), ('ETFS', 'ETFS'), ('Mitsubishi UFJ Kokusai Asst Mgmt Co.,Ltd', 'Mitsubishi UFJ Kokusai Asst Mgmt Co.,Ltd'), ('Rakuten', 'Rakuten'), ('SPDR', 'SPDR'), ('iShares', 'iShares'), ('Nomura', 'Nomura'), ('Asset Management One Co., Ltd.', 'Asset Management One Co., Ltd.'), ('THEAM', 'THEAM'), ('AM-One', 'AM-One'), ('SMAM', 'SMAM'), ('Mitsubishi', 'Mitsubishi'), ('Nomura Asset Management Co Ltd', 'Nomura Asset Management Co Ltd'), ('Daiwa', 'Daiwa'), ('Nikko Asset Management Co Ltd', 'Nikko Asset Management Co Ltd'), ('CSOP', 'CSOP'), ('ChinaAMC', 'ChinaAMC'), ('Daiwa Asset Management Co Ltd', 'Daiwa Asset Management Co Ltd'), ('BlackRock Japan Co Ltd - ETF', 'BlackRock Japan Co Ltd - ETF'), ('State Street Global Adv Singapore Ltd', 'State Street Global Adv Singapore Ltd'), ('NZAM', 'NZAM')], max_length=100),
        ),
        migrations.AlterField(
            model_name='japanfundstaticinfo',
            name='issuer',
            field=models.CharField(choices=[('Shinkin Asset Management Co Ltd', 'Shinkin Asset Management Co Ltd'), ('Okasan Asset Management Co Ltd', 'Okasan Asset Management Co Ltd'), ('FIL Investments (Japan) Limited', 'FIL Investments (Japan) Limited'), ('Rheos Capital Works Inc', 'Rheos Capital Works Inc'), ('Sawakami Asset Management Inc', 'Sawakami Asset Management Inc'), ('Sumitomo Mitsui Trust Asset Management Co., Ltd.', 'Sumitomo Mitsui Trust Asset Management Co., Ltd.'), ('Mitsubishi UFJ Kokusai Asst Mgmt Co.,Ltd', 'Mitsubishi UFJ Kokusai Asst Mgmt Co.,Ltd'), ('UBS Asset Management (Japan) Ltd', 'UBS Asset Management (Japan) Ltd'), ('Nikko Asset Management Co Ltd', 'Nikko Asset Management Co Ltd'), ('Sumitomo Mitsui DS Asset Management Company', 'Sumitomo Mitsui DS Asset Management Company'), ('JPMorgan Asset Management (Japan) Ltd', 'JPMorgan Asset Management (Japan) Ltd'), ('Nissay Asset Management Corporation', 'Nissay Asset Management Corporation'), ('Pictet Asset Management (Japan) Ltd', 'Pictet Asset Management (Japan) Ltd'), ('Asset Management One Co., Ltd.', 'Asset Management One Co., Ltd.'), ('Saison Asset Management Co Ltd', 'Saison Asset Management Co Ltd'), ('Legg Mason Asset Mgmt (Japan) Co Ltd', 'Legg Mason Asset Mgmt (Japan) Co Ltd'), ('Daiwa SB Investments Ltd.', 'Daiwa SB Investments Ltd.'), ('Daiwa Asset Management Co Ltd', 'Daiwa Asset Management Co Ltd'), ('JP Asset Management Co.,Ltd.', 'JP Asset Management Co.,Ltd.'), ('Nomura Asset Management Co Ltd', 'Nomura Asset Management Co Ltd'), ('Sumitomo Mitsui Trust Ast Mgmt Co Ltd', 'Sumitomo Mitsui Trust Ast Mgmt Co Ltd'), ('AllianceBernstein Japan Ltd', 'AllianceBernstein Japan Ltd'), ('Tokio Marine Asset Management Co Ltd', 'Tokio Marine Asset Management Co Ltd'), ('Goldman Sachs Asset Management Co Ltd', 'Goldman Sachs Asset Management Co Ltd')], max_length=100),
        ),
        migrations.AlterField(
            model_name='uketfstaticinfo',
            name='issuer',
            field=models.CharField(choices=[('Deutsche Asset Management', 'Deutsche Asset Management'), ('Pimco', 'Pimco'), ('DB ETC', 'DB ETC'), ('BlackRock', 'BlackRock'), ('Lyxor', 'Lyxor'), ('UBS', 'UBS'), ('ETC', 'ETC'), ('Boost', 'Boost'), ('ETFS', 'ETFS'), ('PowerShares', 'PowerShares'), ('Source', 'Source'), ('HBSC', 'HBSC'), ('DWS Investment S.A.', 'DWS Investment S.A.'), ('VanEck Investments Ltd.', 'VanEck Investments Ltd.'), ('SPDR', 'SPDR'), ('iShares', 'iShares'), ('JPMorgan Asset Management (Europe) S.à r.l.', 'JPMorgan Asset Management (Europe) S.à r.l.'), ('Vanguard Group (Ireland) Limited', 'Vanguard Group (Ireland) Limited'), ('Nomura', 'Nomura'), ('HSBC Investment Funds (Luxembourg) S.A.', 'HSBC Investment Funds (Luxembourg) S.A.'), ('WisdomTree', 'WisdomTree'), ('BlackRock Advisors (UK) Limited - ETF', 'BlackRock Advisors (UK) Limited - ETF'), ('ETFS Oil Securities Ltd', 'ETFS Oil Securities Ltd'), ('BlackRock Asset Management Ireland - ETF', 'BlackRock Asset Management Ireland - ETF'), ('SG', 'SG'), ('Amundi', 'Amundi'), ('Invesco Investment Management Limited', 'Invesco Investment Management Limited'), ('KraneShares', 'KraneShares'), ('PIMCO Global Advisors (Ireland) Limited', 'PIMCO Global Advisors (Ireland) Limited'), ('UBS Fund Management (Luxembourg) S.A.', 'UBS Fund Management (Luxembourg) S.A.'), ('First Trust', 'First Trust'), ('BlackRock Advisors LLC', 'BlackRock Advisors LLC'), ('Fidelity', 'Fidelity'), ('HANetf Management Limited', 'HANetf Management Limited'), ('db X-trackers', 'db X-trackers'), ('LGIM ETF Managers Limited', 'LGIM ETF Managers Limited'), ('X-Trackers', 'X-Trackers'), ('JPMorgan', 'JPMorgan'), ('Vanguard', 'Vanguard'), ('VanEck', 'VanEck'), ('State Street Global Advisors', 'State Street Global Advisors')], max_length=100),
        ),
        migrations.AlterField(
            model_name='ukfundstaticinfo',
            name='issuer',
            field=models.CharField(choices=[('HSBC Investment Funds (Luxembourg) S.A.', 'HSBC Investment Funds (Luxembourg) S.A.'), ('Jupiter Unit Trust Managers Ltd', 'Jupiter Unit Trust Managers Ltd'), ('Vanguard Group (Ireland) Limited', 'Vanguard Group (Ireland) Limited'), ('Vanguard Investments UK, Limited', 'Vanguard Investments UK, Limited'), ('Morgan Stanley Investment Management (ACD) Limited', 'Morgan Stanley Investment Management (ACD) Limited'), ('First State Investment Mgmt (UK) Ltd', 'First State Investment Mgmt (UK) Ltd'), ('Franklin Templeton Investment Funds', 'Franklin Templeton Investment Funds'), ('JPMorgan Asset Management (Europe) S.à r.l.', 'JPMorgan Asset Management (Europe) S.à r.l.'), ('Pictet Asset Management (Europe) SA', 'Pictet Asset Management (Europe) SA'), ('UBP Asset Management (Europe) S.A.', 'UBP Asset Management (Europe) S.A.'), ('Duff & Phelps (Luxembourg) Management Company S.à', 'Duff & Phelps (Luxembourg) Management Company S.à'), ('Lindsell Train Ltd', 'Lindsell Train Ltd'), ('Russell Investments Ireland Limited', 'Russell Investments Ireland Limited'), ('Royal London Asset Management Ltd', 'Royal London Asset Management Ltd'), ('PIMCO Global Advisors (Ireland) Limited', 'PIMCO Global Advisors (Ireland) Limited'), ('BlackRock Asset Management Ireland Ltd', 'BlackRock Asset Management Ireland Ltd'), ('PineBridge Investments Ireland Ltd', 'PineBridge Investments Ireland Ltd'), ('Nordea Investment Funds SA', 'Nordea Investment Funds SA'), ('Capital Group', 'Capital Group'), ('M&G Securities Ltd', 'M&G Securities Ltd'), ('HSBC Global Asset Management (UK) Ltd', 'HSBC Global Asset Management (UK) Ltd'), ('BlackRock Fund Managers Limited', 'BlackRock Fund Managers Limited'), ('Fundsmith LLP', 'Fundsmith LLP'), ('Tokio Marine Asset Management Co Ltd', 'Tokio Marine Asset Management Co Ltd')], max_length=100),
        ),
        migrations.AlterField(
            model_name='usetfstaticinfo',
            name='issuer',
            field=models.CharField(choices=[('Deutsche X-trackers', 'Deutsche X-trackers'), ('Innovator Capital Management LLC', 'Innovator Capital Management LLC'), ('Amplifyetfs', 'Amplifyetfs'), ('ETF Series Solutions', 'ETF Series Solutions'), ('Direxion Funds', 'Direxion Funds'), ('Vanguard', 'Vanguard'), ('Neuberger Berman', 'Neuberger Berman'), ('ALPS', 'ALPS'), ('DoubleLine', 'DoubleLine'), ('SPDR', 'SPDR'), ('Franklin Templeton', 'Franklin Templeton'), ('Fidelity', 'Fidelity'), ('Credit Suisse', 'Credit Suisse'), ('PowerShares', 'PowerShares'), ('VanEck', 'VanEck'), ('Barclays Funds', 'Barclays Funds'), ('ARK', 'ARK'), ('NexPoint Advisors, LP', 'NexPoint Advisors, LP'), ('Sprott', 'Sprott'), ('Direxion', 'Direxion'), ('FlexShares', 'FlexShares'), ('AdvisorShares', 'AdvisorShares'), ('Horizons', 'Horizons'), ('BlackRock', 'BlackRock'), ('Schwab', 'Schwab'), ('First Trust', 'First Trust'), ('USCF Investments', 'USCF Investments'), ('Cambria', 'Cambria'), ('Pacer', 'Pacer'), ('ProShares', 'ProShares'), ('Guggenheim', 'Guggenheim'), ('UBS', 'UBS'), ('IQ', 'IQ'), ('Other', 'Other'), ('Pimco', 'Pimco'), ('Pure Funds', 'Pure Funds'), ('AGFiQ', 'AGFiQ'), ('Oppenheimer', 'Oppenheimer'), ('ETFS', 'ETFS'), ('Global X', 'Global X'), ('Lattice', 'Lattice'), ('VelocityShares', 'VelocityShares'), ('KraneShares', 'KraneShares'), ('iShares', 'iShares'), ('Deutsche Bank', 'Deutsche Bank'), ('Renaissance', 'Renaissance'), ('Strategy shares', 'Strategy shares'), ('WisdomTree', 'WisdomTree'), ('CSOP', 'CSOP'), ('Teucrium', 'Teucrium'), ('Morgan Stanley', 'Morgan Stanley'), ('JPMorgan', 'JPMorgan'), ('ArrowShares', 'ArrowShares'), ('Columbia', 'Columbia'), ('ELEMENTS', 'ELEMENTS')], max_length=100),
        ),
        migrations.AlterField(
            model_name='usfundstaticinfo',
            name='issuer',
            field=models.CharField(choices=[('State Street Global Advisors', 'State Street Global Advisors'), ('Dodge & Cox', 'Dodge & Cox'), ('DoubleLine', 'DoubleLine'), ('Franklin Templeton Investments', 'Franklin Templeton Investments'), ('Fidelity Management Trust Co', 'Fidelity Management Trust Co'), ('T. Rowe Price', 'T. Rowe Price'), ('Pimco', 'Pimco'), ('Schwab Funds', 'Schwab Funds'), ('Prudential Funds (PGIM Investments)', 'Prudential Funds (PGIM Investments)'), ('American Funds', 'American Funds'), ('Vanguard', 'Vanguard'), ('Metropolitan West Funds', 'Metropolitan West Funds'), ('Fidelity Investments', 'Fidelity Investments'), ('Mellon Investments Corporation', 'Mellon Investments Corporation')], max_length=100),
        ),
    ]