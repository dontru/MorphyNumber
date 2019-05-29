from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.SmallIntegerField()),
                ('black', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='black', to='find.Player')),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='find.Result')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='find.Site')),
                ('white', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='white', to='find.Player')),
            ],
        ),
    ]
