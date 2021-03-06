# Generated by Django 2.2.7 on 2019-12-15 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_app', '0059_auto_20191215_1451'),
    ]

    operations = [
        migrations.CreateModel(
            name='AustraliaETFStaticInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=12)),
                ('long_name', models.CharField(max_length=80)),
                ('country', models.CharField(choices=[('G', 'Global'), ('US', 'United States of America'), ('UK', 'United Kingdom'), ('JP', 'Japan'), ('HK', 'Hong Kong'), ('CH', 'China'), ('CA', 'Canada'), ('GE', 'Germany'), ('AU', 'Australia')], default='AU', max_length=2)),
                ('issuer', models.CharField(choices=[('Antipodes Partners Limited', 'Antipodes Partners Limited'), ('InvestSMART Funds Management Ltd', 'InvestSMART Funds Management Ltd'), ('Montgomery Investment Mgmt Pty Ltd', 'Montgomery Investment Mgmt Pty Ltd'), ('The Perth Mint', 'The Perth Mint'), ('Horizons', 'Horizons'), ('ANZ', 'ANZ'), ('Platinum Investment Management Ltd', 'Platinum Investment Management Ltd'), ('SPDR', 'SPDR'), ('K2 Asset Management Ltd', 'K2 Asset Management Ltd'), ('Vanguard Investments Australia Ltd', 'Vanguard Investments Australia Ltd'), ('WCM Investment Management', 'WCM Investment Management'), ('Perennial Investment Management Ltd', 'Perennial Investment Management Ltd'), ('Van Eck', 'Van Eck'), ('Vanguard', 'Vanguard'), ('Other', 'Other'), ('ETFS', 'ETFS'), ('Russell', 'Russell'), ('Fidelity (FIL Fund Management Limited)', 'Fidelity (FIL Fund Management Limited)'), ('ETFS Management (AUS) Ltd', 'ETFS Management (AUS) Ltd'), ('iShares', 'iShares'), ('UBS AU', 'UBS AU'), ('Magellan Asset Management Limited', 'Magellan Asset Management Limited'), ('BetaShares', 'BetaShares')], max_length=38)),
                ('market', models.CharField(choices=[('ASX', 'Australian Securities Exchange')], default='ASX', max_length=3)),
                ('isin', models.CharField(max_length=12)),
                ('link', models.URLField()),
                ('currency', models.CharField(choices=[('USD', 'US Dollar'), ('JPY', 'Japanese Yen'), ('GBP', 'Pound Sterling'), ('HKD', 'Hong Kong Dollar'), ('CNY', 'Chinese Yuan'), ('CAD', 'Canadian Dollar'), ('EUR', 'Euro'), ('AUD', 'Australian Dollar')], default='AUD', max_length=3)),
            ],
            options={
                'verbose_name': "Australia ETFs' Static Info",
                'verbose_name_plural': "Australia ETFs' Static Info",
            },
        ),
        migrations.CreateModel(
            name='CanadaETFStaticInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=12)),
                ('long_name', models.CharField(max_length=80)),
                ('country', models.CharField(choices=[('G', 'Global'), ('US', 'United States of America'), ('UK', 'United Kingdom'), ('JP', 'Japan'), ('HK', 'Hong Kong'), ('CH', 'China'), ('CA', 'Canada'), ('GE', 'Germany'), ('AU', 'Australia')], default='CA', max_length=2)),
                ('issuer', models.CharField(choices=[('Mackenzie', 'Mackenzie'), ('First Block Capital', 'First Block Capital'), ('Bristol Gate Capital Partners', 'Bristol Gate Capital Partners'), ('Sprott', 'Sprott'), ('Emerge Canada Inc.', 'Emerge Canada Inc.'), ('PowerShares', 'PowerShares'), ('Manulife Investments', 'Manulife Investments'), ('National Bank Investments Inc', 'National Bank Investments Inc'), ('Horizons', 'Horizons'), ('BlackRock', 'BlackRock'), ('Franklin Templeton Investments Corp', 'Franklin Templeton Investments Corp'), ('Evolve Funds Group Inc.', 'Evolve Funds Group Inc.'), ('Accelerate Financial Tech Inc', 'Accelerate Financial Tech Inc'), ('RBC Global', 'RBC Global'), ('Hamilton Capital Partners', 'Hamilton Capital Partners'), ('Pimco', 'Pimco'), ('First Asset', 'First Asset'), ('Fidelity', 'Fidelity'), ('Fidelity Investments Canada ULC', 'Fidelity Investments Canada ULC'), ('Questrade', 'Questrade'), ('Purpose', 'Purpose'), ('Harvest', 'Harvest'), ('QuantShares', 'QuantShares'), ('RBS', 'RBS'), ('Harvest Portfolios Group Inc.', 'Harvest Portfolios Group Inc.'), ('SmartBe Wealth Inc', 'SmartBe Wealth Inc'), ('Vanguard', 'Vanguard'), ('Picton Mahoney Asset Management', 'Picton Mahoney Asset Management'), ('Other', 'Other'), ('Auspice Capital Advisors', 'Auspice Capital Advisors'), ('Coin Capital Investment Inc.', 'Coin Capital Investment Inc.'), ('Invesco Canada Ltd.', 'Invesco Canada Ltd.'), ('Brompton Funds', 'Brompton Funds'), ('Purpose Investments Inc.', 'Purpose Investments Inc.'), ('Franklin Templeton', 'Franklin Templeton'), ('Franklin Templeton Investments', 'Franklin Templeton Investments'), ('Desjardins Global Asset Management', 'Desjardins Global Asset Management'), ('First Trust', 'First Trust'), ('Vanguard Investments Canada Inc', 'Vanguard Investments Canada Inc'), ('Lysander Funds Ltd.', 'Lysander Funds Ltd.'), ('TD AM', 'TD AM'), ('Sphere Investment Management Inc', 'Sphere Investment Management Inc'), ('WisdomTree', 'WisdomTree'), ('CIBC Asset Management Inc', 'CIBC Asset Management Inc'), ('TD Asset Management', 'TD Asset Management'), ('BlackRock Asset Management Canada Ltd', 'BlackRock Asset Management Canada Ltd'), ('iShares', 'iShares'), ('AGF Investments Inc.', 'AGF Investments Inc.'), ('Starlight Investments Capital LP', 'Starlight Investments Capital LP'), ('PIMCO Canada', 'PIMCO Canada'), ('First Asset Investment Management Inc', 'First Asset Investment Management Inc'), ('BMO', 'BMO')], max_length=37)),
                ('market', models.CharField(choices=[('NEO', 'Aequitas Neo Exchange (NEO)'), ('Toronto', 'Toronto Stock Exchange (TSX)'), ('CSE', 'Canadian Securities Exchange (CSE)'), ('NASDAQ', 'NASDAQ Canada'), ('TSXV', 'TSX Venture Exchange (TSXV)')], max_length=7)),
                ('isin', models.CharField(max_length=12)),
                ('link', models.URLField()),
                ('currency', models.CharField(choices=[('USD', 'US Dollar'), ('JPY', 'Japanese Yen'), ('GBP', 'Pound Sterling'), ('HKD', 'Hong Kong Dollar'), ('CNY', 'Chinese Yuan'), ('CAD', 'Canadian Dollar'), ('EUR', 'Euro'), ('AUD', 'Australian Dollar')], default='CAD', max_length=3)),
            ],
            options={
                'verbose_name': "Canada ETFs' Static Info",
                'verbose_name_plural': "Canada ETFs' Static Info",
            },
        ),
        migrations.CreateModel(
            name='ChinaETFStaticInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=12)),
                ('long_name', models.CharField(max_length=80)),
                ('country', models.CharField(choices=[('G', 'Global'), ('US', 'United States of America'), ('UK', 'United Kingdom'), ('JP', 'Japan'), ('HK', 'Hong Kong'), ('CH', 'China'), ('CA', 'Canada'), ('GE', 'Germany'), ('AU', 'Australia')], default='CH', max_length=2)),
                ('issuer', models.CharField(choices=[('CCB Principal Asset Mgmt Co.,Ltd', 'CCB Principal Asset Mgmt Co.,Ltd'), ('Fortune SG Fund Management CO.,Ltd', 'Fortune SG Fund Management CO.,Ltd'), ('AXA SPDB Investment Managers Co.,Ltd', 'AXA SPDB Investment Managers Co.,Ltd'), ('New China Fund Mgmt Co.,Ltd', 'New China Fund Mgmt Co.,Ltd'), ('Invesco', 'Invesco'), ('ICBC Credit Suisse Asset Mgmt Co.,Ltd', 'ICBC Credit Suisse Asset Mgmt Co.,Ltd'), ('Invesco Great Wall Fund Mgmt Co. Ltd', 'Invesco Great Wall Fund Mgmt Co. Ltd'), ('Golden Eagle Asset Management Co.,Ltd', 'Golden Eagle Asset Management Co.,Ltd'), ('Ping An Fund Management Company Limited', 'Ping An Fund Management Company Limited'), ('Wanjia Asset Mgmt Co., Ltd', 'Wanjia Asset Mgmt Co., Ltd'), ('CIB Fund Management Co.,Ltd', 'CIB Fund Management Co.,Ltd'), ('Horizons', 'Horizons'), ('Huatai-PB', 'Huatai-PB'), ('China Merchants Fund Mgmt Co.,Ltd', 'China Merchants Fund Mgmt Co.,Ltd'), ('Huatai-PineBridge Fund Mgmt Co., Ltd', 'Huatai-PineBridge Fund Mgmt Co., Ltd'), ('Ping An UOB Fund Management Company Ltd', 'Ping An UOB Fund Management Company Ltd'), ('Ping An of China Asset Management (HK)Co', 'Ping An of China Asset Management (HK)Co'), ('Yinhua Fund Mgmt Co., Ltd', 'Yinhua Fund Mgmt Co., Ltd'), ('China Southern Fund Mgmt Co.,Ltd', 'China Southern Fund Mgmt Co.,Ltd'), ('Bosera', 'Bosera'), ('Harvest Fund Mgmt Co.,Ltd', 'Harvest Fund Mgmt Co.,Ltd'), ('E Fund', 'E Fund'), ('China Asset Management Co., Ltd.', 'China Asset Management Co., Ltd.'), ('Harvest', 'Harvest'), ('GuoTai', 'GuoTai'), ('GF Fund Mgmt Co.,Ltd', 'GF Fund Mgmt Co.,Ltd'), ('HuaAn', 'HuaAn'), ('China Universal Asset Mgmt Co.Ltd', 'China Universal Asset Mgmt Co.Ltd'), ('Fortune SG', 'Fortune SG'), ('Other', 'Other'), ('HuaAn Fund Mgmt Co., Ltd', 'HuaAn Fund Mgmt Co., Ltd'), ('Lion Fund Mgmt Co.,Ltd', 'Lion Fund Mgmt Co.,Ltd'), ('ChinaAMC', 'ChinaAMC'), ('SWS MU Fund Management Co., Ltd', 'SWS MU Fund Management Co., Ltd'), ('Bank of Communications Schroders', 'Bank of Communications Schroders'), ('HFT Investment Mgmt Co., Ltd', 'HFT Investment Mgmt Co., Ltd'), ('China Asset Mgmt Co.,Ltd', 'China Asset Mgmt Co.,Ltd'), ('Hony Horizon Fund Management Co.,ltd', 'Hony Horizon Fund Management Co.,ltd'), ('Penghua Fund Mgmt Co.,Ltd', 'Penghua Fund Mgmt Co.,Ltd'), ('China Southern', 'China Southern'), ('Fubon', 'Fubon'), ('Founder & Fubon Fund Mngmt Co., Ltd.', 'Founder & Fubon Fund Mngmt Co., Ltd.'), ('China Life AMP Asset Management Co.Ltd', 'China Life AMP Asset Management Co.Ltd'), ('DaCheng', 'DaCheng'), ('Guotai Asset Mgmt Co.,Ltd', 'Guotai Asset Mgmt Co.,Ltd'), ('Fullgoal Fund Mgmt Co.,Ltd', 'Fullgoal Fund Mgmt Co.,Ltd'), ('GTJA-Allianz Fund Mgmt Co.,Ltd', 'GTJA-Allianz Fund Mgmt Co.,Ltd'), ('China Fund Management Co. Ltd.', 'China Fund Management Co. Ltd.'), ('Hwabao WP Fund Management Co.,Ltd', 'Hwabao WP Fund Management Co.,Ltd'), ('Nanhua', 'Nanhua'), ('Bank of China Investment Mgmt Co.,Ltd', 'Bank of China Investment Mgmt Co.,Ltd')], max_length=40)),
                ('market', models.CharField(choices=[('Shanghai', 'Shanghai Stock Exchange'), ('Shenzhen', 'Shenzhen Stock Exchange')], max_length=20)),
                ('isin', models.CharField(max_length=12)),
                ('link', models.URLField()),
                ('currency', models.CharField(choices=[('USD', 'US Dollar'), ('JPY', 'Japanese Yen'), ('GBP', 'Pound Sterling'), ('HKD', 'Hong Kong Dollar'), ('CNY', 'Chinese Yuan'), ('CAD', 'Canadian Dollar'), ('EUR', 'Euro'), ('AUD', 'Australian Dollar')], default='CNY', max_length=3)),
            ],
            options={
                'verbose_name': "China ETFs' Static Info",
                'verbose_name_plural': "China ETFs' Static Info",
            },
        ),
        migrations.CreateModel(
            name='GermanyETFStaticInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=12)),
                ('long_name', models.CharField(max_length=80)),
                ('country', models.CharField(choices=[('G', 'Global'), ('US', 'United States of America'), ('UK', 'United Kingdom'), ('JP', 'Japan'), ('HK', 'Hong Kong'), ('CH', 'China'), ('CA', 'Canada'), ('GE', 'Germany'), ('AU', 'Australia')], default='GE', max_length=2)),
                ('issuer', models.CharField(choices=[('Lyxor', 'Lyxor'), ('HBSC', 'HBSC'), ('PowerShares', 'PowerShares'), ('Deka', 'Deka'), ('BlackRock', 'BlackRock'), ('Amundi', 'Amundi'), ('Pimco', 'Pimco'), ('SPDR', 'SPDR'), ('DB ETC', 'DB ETC'), ('Ossiam', 'Ossiam'), ('Deutsche Börse Commodities GmbH', 'Deutsche Börse Commodities GmbH'), ('Commerzbank AG', 'Commerzbank AG'), ('UBS UK', 'UBS UK'), ('Boost', 'Boost'), ('UBS', 'UBS'), ('Other', 'Other'), ('ETFS', 'ETFS'), ('BNP Paribas', 'BNP Paribas'), ('X-Trackers', 'X-Trackers'), ('BlackRock Asset Management Ireland - ETF', 'BlackRock Asset Management Ireland - ETF'), ('db X-trackers', 'db X-trackers'), ('First Trust', 'First Trust'), ('Source', 'Source'), ('ComStage', 'ComStage'), ('WisdomTree', 'WisdomTree'), ('THEAM', 'THEAM'), ('iShares', 'iShares'), ('RBS', 'RBS')], max_length=40)),
                ('market', models.CharField(choices=[('Frankfurt', 'Frankfurt Stock Exchange (XFRA)'), ('Berlin', 'Berlin Stock Exchange (XBER)'), ('Xetra', 'Xetra Stock Exchange (XETR)'), ('Munich', 'Munich Stock Exchange (XMUN)'), ('Stuttgart', 'Stuttgart Stock Exchange (XSTU)'), ('Dusseldorf', 'Dusseldorf Stock Exchange(XDUS)'), ('Hamburg', 'Hamburg Stock Exchange(XHAM)'), ('Hannover', 'Hannover Stock Exchange (XHAN)')], max_length=20)),
                ('isin', models.CharField(max_length=12)),
                ('link', models.URLField()),
                ('currency', models.CharField(choices=[('USD', 'US Dollar'), ('JPY', 'Japanese Yen'), ('GBP', 'Pound Sterling'), ('HKD', 'Hong Kong Dollar'), ('CNY', 'Chinese Yuan'), ('CAD', 'Canadian Dollar'), ('EUR', 'Euro'), ('AUD', 'Australian Dollar')], default='EUR', max_length=3)),
            ],
            options={
                'verbose_name': "Germany ETFs' Static Info",
                'verbose_name_plural': "Germany ETFs' Static Info",
            },
        ),
        migrations.CreateModel(
            name='HKETFStaticInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=12)),
                ('long_name', models.CharField(max_length=80)),
                ('country', models.CharField(choices=[('G', 'Global'), ('US', 'United States of America'), ('UK', 'United Kingdom'), ('JP', 'Japan'), ('HK', 'Hong Kong'), ('CH', 'China'), ('CA', 'Canada'), ('GE', 'Germany'), ('AU', 'Australia')], default='HK', max_length=2)),
                ('issuer', models.CharField(choices=[('State Street Global Advisors Asia Ltd', 'State Street Global Advisors Asia Ltd'), ('W.I.S.E', 'W.I.S.E'), ('Mirae Asset', 'Mirae Asset'), ('Samsung', 'Samsung'), ('Horizons', 'Horizons'), ('Hai Tong', 'Hai Tong'), ('China Universal Asset Management (HK) Limited', 'China Universal Asset Management (HK) Limited'), ('Amundi', 'Amundi'), ('SPDR', 'SPDR'), ('Bosera', 'Bosera'), ('State Street Global Advisors', 'State Street Global Advisors'), ('E Fund', 'E Fund'), ('Harvest', 'Harvest'), ('China Asset Management (HK) Limited', 'China Asset Management (HK) Limited'), ('Vanguard', 'Vanguard'), ('GFI', 'GFI'), ('Other', 'Other'), ('Lippo Investments Management Limited', 'Lippo Investments Management Limited'), ('ChinaAMC', 'ChinaAMC'), ('Premia Partners Company Limited', 'Premia Partners Company Limited'), ('db X-trackers', 'db X-trackers'), ('China International Capital Corporation', 'China International Capital Corporation'), ('CSOP Asset Management Limited', 'CSOP Asset Management Limited'), ('China Intl Capital Corp HK Asse Mgt Ltd.', 'China Intl Capital Corp HK Asse Mgt Ltd.'), ('E Fund Management (HK) Co., Ltd', 'E Fund Management (HK) Co., Ltd'), ('ComStage', 'ComStage'), ('CSOP', 'CSOP'), ('HSBC Investment Funds (HK) Limited', 'HSBC Investment Funds (HK) Limited'), ('Value', 'Value'), ('iShares', 'iShares'), ('Hang Seng', 'Hang Seng'), ('Yuanta', 'Yuanta'), ('BMO', 'BMO')], max_length=45)),
                ('market', models.CharField(choices=[('HKG', 'The Stock Exchange of Hong Kong Limited')], default='HKG', max_length=3)),
                ('isin', models.CharField(max_length=12)),
                ('link', models.URLField()),
                ('currency', models.CharField(choices=[('USD', 'US Dollar'), ('JPY', 'Japanese Yen'), ('GBP', 'Pound Sterling'), ('HKD', 'Hong Kong Dollar'), ('CNY', 'Chinese Yuan'), ('CAD', 'Canadian Dollar'), ('EUR', 'Euro'), ('AUD', 'Australian Dollar')], default='HKD', max_length=3)),
            ],
            options={
                'verbose_name': "Honk Kong ETFs' Static Info",
                'verbose_name_plural': "Honk Kong ETFs' Static Info",
            },
        ),
        migrations.CreateModel(
            name='JapanETFStaticInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=12)),
                ('long_name', models.CharField(max_length=80)),
                ('country', models.CharField(choices=[('G', 'Global'), ('US', 'United States of America'), ('UK', 'United Kingdom'), ('JP', 'Japan'), ('HK', 'Hong Kong'), ('CH', 'China'), ('CA', 'Canada'), ('GE', 'Germany'), ('AU', 'Australia')], default='JP', max_length=2)),
                ('issuer', models.CharField(choices=[('Samsung', 'Samsung'), ('SMAM', 'SMAM'), ('Mitsubishi', 'Mitsubishi'), ('Daiwa', 'Daiwa'), ('AM-One', 'AM-One'), ('SPDR', 'SPDR'), ('Nomura', 'Nomura'), ('Rakuten', 'Rakuten'), ('Simplex', 'Simplex'), ('Norinchukin Zenkyoren Asset Mgmt Co.,Ltd', 'Norinchukin Zenkyoren Asset Mgmt Co.,Ltd'), ('UBS', 'UBS'), ('ETFS', 'ETFS'), ('ChinaAMC', 'ChinaAMC'), ('Daiwa Asset Management Co Ltd', 'Daiwa Asset Management Co Ltd'), ('NZAM', 'NZAM'), ('Asset Management One Co., Ltd.', 'Asset Management One Co., Ltd.'), ('Nikko Asset Management Co Ltd', 'Nikko Asset Management Co Ltd'), ('CSOP', 'CSOP'), ('BlackRock Japan Co Ltd', 'BlackRock Japan Co Ltd'), ('Nikko', 'Nikko'), ('THEAM', 'THEAM'), ('iShares', 'iShares'), ('State Street Global Adv Singapore Ltd', 'State Street Global Adv Singapore Ltd'), ('Mitsubishi UFJ Kokusai Asst Mgmt Co.,Ltd', 'Mitsubishi UFJ Kokusai Asst Mgmt Co.,Ltd'), ('Nomura Asset Management Co Ltd', 'Nomura Asset Management Co Ltd')], max_length=40)),
                ('market', models.CharField(choices=[('Tokyo', 'Tokyo Stock Exchange (TYO)'), ('Osaka', 'Osaka Securities Exchange'), ('Nagoya', 'Nagoya Stock Exchange (NSE)'), ('Fukuoka', 'Fukuoka Stock Exchange (FSE)'), ('Sapporo', 'Sapporo Securities Exchange'), ('JASDAQ', 'JASDAQ Securities Exchange')], max_length=7)),
                ('isin', models.CharField(max_length=12)),
                ('link', models.URLField()),
                ('currency', models.CharField(choices=[('USD', 'US Dollar'), ('JPY', 'Japanese Yen'), ('GBP', 'Pound Sterling'), ('HKD', 'Hong Kong Dollar'), ('CNY', 'Chinese Yuan'), ('CAD', 'Canadian Dollar'), ('EUR', 'Euro'), ('AUD', 'Australian Dollar')], default='JPY', max_length=3)),
            ],
            options={
                'verbose_name': "Japan ETFs' Static Info",
                'verbose_name_plural': "Japan ETFs' Static Info",
            },
        ),
        migrations.CreateModel(
            name='UKETFStaticInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=12)),
                ('long_name', models.CharField(max_length=80)),
                ('country', models.CharField(choices=[('G', 'Global'), ('US', 'United States of America'), ('UK', 'United Kingdom'), ('JP', 'Japan'), ('HK', 'Hong Kong'), ('CH', 'China'), ('CA', 'Canada'), ('GE', 'Germany'), ('AU', 'Australia')], default='UK', max_length=2)),
                ('issuer', models.CharField(choices=[('Lyxor', 'Lyxor'), ('HBSC', 'HBSC'), ('PowerShares', 'PowerShares'), ('XBT Provider AB', 'XBT Provider AB'), ('JPMorgan', 'JPMorgan'), ('Amundi', 'Amundi'), ('HSBC Investment Funds (Luxembourg) S.A.', 'HSBC Investment Funds (Luxembourg) S.A.'), ('Pimco', 'Pimco'), ('Fidelity', 'Fidelity'), ('SPDR', 'SPDR'), ('DB ETC', 'DB ETC'), ('Ossiam', 'Ossiam'), ('ETC', 'ETC'), ('Nomura', 'Nomura'), ('Van Eck', 'Van Eck'), ('UBS UK', 'UBS UK'), ('Boost', 'Boost'), ('UBS', 'UBS'), ('Vanguard', 'Vanguard'), ('ETFS', 'ETFS'), ('X-Trackers', 'X-Trackers'), ('BlackRock Asset Management Ireland - ETF', 'BlackRock Asset Management Ireland - ETF'), ('db X-trackers', 'db X-trackers'), ('SG', 'SG'), ('LGIM ETF Managers Limited', 'LGIM ETF Managers Limited'), ('First Trust', 'First Trust'), ('UBS Fund Management (Luxembourg) S.A.', 'UBS Fund Management (Luxembourg) S.A.'), ('Source', 'Source'), ('WisdomTree', 'WisdomTree'), ('Fundlogic', 'Fundlogic'), ('iShares', 'iShares'), ('BMO', 'BMO')], max_length=40)),
                ('market', models.CharField(choices=[('London', 'London Stock Exchange')], default='London', max_length=20)),
                ('isin', models.CharField(max_length=12)),
                ('link', models.URLField()),
                ('currency', models.CharField(choices=[('USD', 'US Dollar'), ('JPY', 'Japanese Yen'), ('GBP', 'Pound Sterling'), ('HKD', 'Hong Kong Dollar'), ('CNY', 'Chinese Yuan'), ('CAD', 'Canadian Dollar'), ('EUR', 'Euro'), ('AUD', 'Australian Dollar')], default='GBP', max_length=3)),
            ],
            options={
                'verbose_name': "United Kingdom ETFs' Static Info",
                'verbose_name_plural': "United Kingdom ETFs' Static Info",
            },
        ),
        migrations.CreateModel(
            name='USETFStaticInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=12)),
                ('long_name', models.CharField(max_length=80)),
                ('country', models.CharField(choices=[('G', 'Global'), ('US', 'United States of America'), ('UK', 'United Kingdom'), ('JP', 'Japan'), ('HK', 'Hong Kong'), ('CH', 'China'), ('CA', 'Canada'), ('GE', 'Germany'), ('AU', 'Australia')], max_length=2)),
                ('issuer', models.CharField(max_length=32)),
                ('market', models.CharField(choices=[('NYSE', 'New York Stock Exchange (NYSE)'), ('NASDAQ', 'NASDAQ Stock Market'), ('OTC Markets', 'Over-The-Counter Markets (OTC)'), ('AMEX', 'American Stock Exchange (AMEX)'), ('BSE', 'Boston Stock Exchange (BSE)'), ('CBOE', 'Chicago Board Options Exchange (CBOE)'), ('CBOT', 'Chicago Board of Trade (CBOT)'), ('CME', 'Chicago Mercantile Exchange (CME)'), ('CHX', 'Chicago Stock Exchange (CHX)'), ('ISE', 'International Securities Exchange i.nameSE)'), ('MS4X', 'Miami Stock Exchange (MS4X)'), ('NSX', 'National Stock Exchange (NSX)'), ('PHLX', 'Philadelphia Stock Exchange (PHLX)'), ('NYSE Arca', 'NYSE Arca')], max_length=11)),
                ('currency', models.CharField(choices=[('USD', 'US Dollar'), ('JPY', 'Japanese Yen'), ('GBP', 'Pound Sterling'), ('HKD', 'Hong Kong Dollar'), ('CNY', 'Chinese Yuan'), ('CAD', 'Canadian Dollar'), ('EUR', 'Euro'), ('AUD', 'Australian Dollar')], default='USD', max_length=3)),
                ('isin', models.CharField(max_length=12)),
                ('link', models.URLField()),
            ],
            options={
                'verbose_name': "United States ETFs' Static Info",
                'verbose_name_plural': "United States ETFs' Static Info",
            },
        ),
    ]
