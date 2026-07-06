import math
import numpy as np


class SimuladorQuinua:

    def __init__(self):
        pass

    def simular(self, area, semilla_densidad, riego_frecuencia, fertilizante_npk, temperatura_media):
        """
        Simula el crecimiento y producción de quinua durante un ciclo de 150 días.
        
        Parámetros:
        - area: Área total sembrada en hectáreas
        - semilla_densidad: Densidad de semilla en kg/ha
        - riego_frecuencia: Frecuencia de riego en días (ej. 7 significa regar cada 7 días)
        - fertilizante_npk: Cantidad de fertilizante NPK aplicado en kg/ha
        - temperatura_media: Temperatura media ambiental promedio del ciclo en °C
        
        Retorna:
        - dias: Lista con los días de simulación [1..150]
        - biomasa: Lista con la biomasa acumulada en kg/ha día a día
        - grano: Lista con el peso del grano en kg/ha día a día
        - balance: Diccionario con estadísticas finales del proyecto (costos, ingresos, rendimiento)
        """
        ciclo_dias = 150
        dias = list(range(1, ciclo_dias + 1))
        
        # Vectores de almacenamiento diario
        biomasa = []
        grano = []
        
        # Estado de humedad del suelo (0% a 100% de capacidad de campo)
        humedad_suelo = 100.0
        
        # Biomasa acumulada inicial
        biomasa_acum = 0.0
        grano_acum = 0.0
        
        # Factor de nutrientes fijo basado en NPK (Óptimo es 120 kg/ha)
        f_nutrientes = 0.4 + 0.6 * min(fertilizante_npk / 120.0, 1.0)
        
        # Temperatura óptima para la quinua es ~18°C
        # Tasa de crecimiento disminuye si se aleja de la temperatura óptima
        f_temperatura = math.exp(-0.05 * (temperatura_media - 18.0) ** 2)
        
        # Efecto de la densidad de semillas: densidad óptima es entre 8 y 12 kg/ha.
        # Muy poco o demasiado reduce la eficiencia.
        if semilla_densidad < 8.0:
            f_densidad = semilla_densidad / 8.0
        elif semilla_densidad > 12.0:
            f_densidad = max(0.5, 1.0 - (semilla_densidad - 12.0) * 0.05)
        else:
            f_densidad = 1.0

        for dia in dias:
            # --- Simulación del agua del suelo ---
            # Evapotranspiración diaria (pérdida de agua)
            evapotranspiracion = 3.5 + 0.1 * temperatura_media
            humedad_suelo -= evapotranspiracion
            
            # Aplicar riego
            if dia % riego_frecuencia == 0:
                humedad_suelo += 30.0  # Riego aporta humedad
            
            # Limitar humedad
            humedad_suelo = max(0.0, min(100.0, humedad_suelo))
            
            # Factor de estrés hídrico (si la humedad es menor al 30%, hay estrés)
            if humedad_suelo >= 30.0:
                f_agua = 1.0
            else:
                f_agua = humedad_suelo / 30.0
                
            # --- Crecimiento Diario de Biomasa ---
            # El crecimiento potencial sigue una curva logística respecto a los días (desarrollo foliar)
            # Fase vegetativa máxima ocurre alrededor del día 70
            tasa_crecimiento_base = 120.0 / (1.0 + math.exp(-0.08 * (dia - 60)))
            
            # Crecimiento real del día
            crecimiento_dia = tasa_crecimiento_base * f_temperatura * f_agua * f_nutrientes * f_densidad
            
            # Germinación (primeros 10 días): el crecimiento de biomasa aérea es muy pequeño
            if dia <= 10:
                crecimiento_dia *= 0.1
                
            biomasa_acum += crecimiento_dia
            biomasa.append(biomasa_acum)
            
            # --- Llenado de Grano ---
            # Ocurre principalmente en el último tercio del ciclo (días 90 a 140)
            if dia > 90 and dia <= 140:
                # Translocación a grano (Harvest Index progresa hasta ~0.4)
                incremento_grano = crecimiento_dia * 0.45 + (biomasa_acum * 0.005)
                grano_acum += incremento_grano
            elif dia > 140:
                # Etapa de secado/madurez: el grano deja de ganar peso y se estabiliza
                pass
            else:
                grano_acum = 0.0
                
            grano.append(grano_acum)

        # Rendimientos finales (kg por hectárea)
        rendimiento_biomasa_ha = biomasa[-1]
        rendimiento_grano_ha = grano[-1]
        
        # Rendimiento total del campo (toneladas)
        rendimiento_total_ton = (rendimiento_grano_ha * area) / 1000.0
        
        # --- ANÁLISIS FINANCIERO ---
        # Costo unitarios aproximados
        costo_semilla_por_kg = 4.5  # USD/kg de semilla certificada
        costo_fertilizante_por_kg = 1.2  # USD/kg de NPK
        costo_riego_por_dia = 25.0  # USD por riego por hectárea
        costo_mano_obra_ha = 600.0  # USD preparación de suelo, siembra y cosecha por hectárea
        
        # Calcular costos totales
        costo_semillas = area * semilla_densidad * costo_semilla_por_kg
        costo_fertilizacion = area * fertilizante_npk * costo_fertilizante_por_kg
        
        num_riegos = ciclo_dias // riego_frecuencia
        costo_agua = area * num_riegos * costo_riego_por_dia
        costo_operativo = area * costo_mano_obra_ha
        
        costo_total = costo_semillas + costo_fertilizacion + costo_agua + costo_operativo
        
        # Precio de venta del grano de quinua (USD/kg)
        precio_quinua_kg = 2.80  # USD/kg en mercado de exportación
        ingreso_total = (rendimiento_grano_ha * area) * precio_quinua_kg
        
        ganancia_neta = ingreso_total - costo_total
        retorno_inversion = (ganancia_neta / costo_total) * 100.0 if costo_total > 0 else 0.0

        balance = {
            "rendimiento_ha": rendimiento_grano_ha,
            "produccion_total": rendimiento_total_ton,
            "costo_semillas": costo_semillas,
            "costo_fertilizantes": costo_fertilizacion,
            "costo_agua": costo_agua,
            "costo_operativo": costo_operativo,
            "costo_total": costo_total,
            "ingresos_totales": ingreso_total,
            "ganancia_neta": ganancia_neta,
            "roi": retorno_inversion
        }

        return dias, biomasa, grano, balance
