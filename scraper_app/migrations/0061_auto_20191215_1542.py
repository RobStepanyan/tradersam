# Generated by Django 2.2.7 on 2019-12-15 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_app', '0060_australiaetfstaticinfo_canadaetfstaticinfo_chinaetfstaticinfo_germanyetfstaticinfo_hketfstaticinfo_j'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usetfstaticinfo',
            name='issuer',
            field=models.CharField(choices=[('Vanguard', 'Vanguard'), ('Strategy shares', 'Strategy shares'), ('Deutsche Bank', 'Deutsche Bank'), ('IQ', 'IQ'), ('Fidelity', 'Fidelity'), ('SPDR', 'SPDR'), ('ETF Series Solutions', 'ETF Series Solutions'), ('Horizons', 'Horizons'), ('CSOP', 'CSOP'), ('JPMorgan', 'JPMorgan'), ('ELEMENTS', 'ELEMENTS'), ('iShares', 'iShares'), ('Credit Suisse', 'Credit Suisse'), ('KraneShares', 'KraneShares'), ('Guggenheim', 'Guggenheim'), ('Oppenheimer', 'Oppenheimer'), ('ETFS', 'ETFS'), ('Columbia', 'Columbia'), ('Pimco', 'Pimco'), ('PowerShares', 'PowerShares'), ('UBS', 'UBS'), ('Pacer', 'Pacer'), ('ALPS', 'ALPS'), ('Lattice', 'Lattice'), ('Innovator Capital Management LLC', 'Innovator Capital Management LLC'), ('Direxion', 'Direxion'), ('Goldman Sachs', 'Goldman Sachs'), ('FlexShares', 'FlexShares'), ('Morgan Stanley', 'Morgan Stanley'), ('Citigroup', 'Citigroup'), ('ProShares', 'ProShares'), ('WisdomTree', 'WisdomTree'), ('ARK', 'ARK'), ('BlackRock', 'BlackRock'), ('Van Eck', 'Van Eck'), ('AdvisorShares', 'AdvisorShares'), ('Deutsche X-trackers', 'Deutsche X-trackers'), ('Franklin Templeton', 'Franklin Templeton'), ('First Trust', 'First Trust'), ('NexPoint Advisors, LP', 'NexPoint Advisors, LP'), ('Global X', 'Global X'), ('QuantShares', 'QuantShares'), ('VelocityShares', 'VelocityShares'), ('DoubleLine', 'DoubleLine'), ('Schwab', 'Schwab'), ('Renaissance', 'Renaissance'), ('Pure Funds', 'Pure Funds'), ('Teucrium', 'Teucrium'), ('Sprott', 'Sprott'), ('Cambria', 'Cambria'), ('ArrowShares', 'ArrowShares'), ('Neuberger Berman', 'Neuberger Berman'), ('USCF', 'USCF'), ('Barclays Funds', 'Barclays Funds'), ('Other', 'Other')], max_length=32),
        ),
    ]
