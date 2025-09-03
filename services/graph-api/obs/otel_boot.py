import os

DISABLED = str(os.getenv("OTEL_SDK_DISABLED","" )).lower() in {"1","true","yes"}

# Wenn OTEL disabled ist: ruhig bleiben und NICHT initialisieren.
if DISABLED:
    # bewusst keine Initialisierung; Import der Datei soll folgenlos sein
    INSTRUMENTATION_ENABLED = False
else:
    # Beispiel: hier würde regulär initialisiert (SDK, exporter, instrumentors)
    # Im Dev-Kontext bleibt das leer, Prod füllt das aus.
    INSTRUMENTATION_ENABLED = True
