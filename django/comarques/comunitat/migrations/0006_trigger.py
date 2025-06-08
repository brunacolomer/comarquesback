from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('comunitat', '0005_alter_amistat_foto'),  # Substitueix per la darrera migració
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE OR REPLACE FUNCTION actualitza_puntuacio_amistat()
            RETURNS TRIGGER AS $$
            DECLARE
                comarca1 TEXT;
                comarca2 TEXT;
                habitants1 INTEGER;
                habitants2 INTEGER;
                distancia FLOAT;
                punts1 INTEGER;
                punts2 INTEGER;
            BEGIN
                SELECT p.comarca_id INTO comarca1
                FROM comunitat_usuari u
                JOIN comunitat_poblacio p ON u.poblacio_id = p.nom
                WHERE u.id = NEW.usuari1_id;

                SELECT p.comarca_id INTO comarca2
                FROM comunitat_usuari u
                JOIN comunitat_poblacio p ON u.poblacio_id = p.nom
                WHERE u.id = NEW.usuari2_id;

                IF comarca1 = comarca2 THEN
                    RETURN NEW;
                END IF;

                SELECT habitants INTO habitants2 FROM comunitat_comarca WHERE nom = comarca2;
                SELECT habitants INTO habitants1 FROM comunitat_comarca WHERE nom = comarca1;

                SELECT d.distancia INTO distancia
                FROM comunitat_distancia d
                WHERE LEAST(d.comarca1_id, d.comarca2_id) = LEAST(comarca1, comarca2)
                  AND GREATEST(d.comarca1_id, d.comarca2_id) = GREATEST(comarca1, comarca2);

                SELECT CEIL(500000.0 / habitants2) + FLOOR(distancia * 0.75) INTO punts1;
                SELECT CEIL(500000.0 / habitants1) + FLOOR(distancia * 0.75) INTO punts2;

                UPDATE comunitat_usuari SET puntuacio = puntuacio + punts1 WHERE id = NEW.usuari1_id;
                UPDATE comunitat_usuari SET puntuacio = puntuacio + punts2 WHERE id = NEW.usuari2_id;

                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;

            CREATE TRIGGER trigger_recalcula_puntuacio
            AFTER INSERT ON comunitat_amistat
            FOR EACH ROW
            EXECUTE FUNCTION actualitza_puntuacio_amistat();
            """,
            reverse_sql="""
            DROP TRIGGER IF EXISTS trigger_recalcula_puntuacio ON comunitat_amistat;
            DROP FUNCTION IF EXISTS actualitza_puntuacio_amistat;
            """
        )
    ]
