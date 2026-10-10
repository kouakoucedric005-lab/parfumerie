"""Middleware de sécurité renforcée pour l'application Django Parfumerie."""

class SecurityHeadersMiddleware:
    """Ajoute des en-têtes HTTP de sécurité stricts à chaque réponse."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # En-têtes HTTP de sécurité renforcés
        response["X-Content-Type-Options"] = "nosniff"
        response["X-Frame-Options"] = "DENY"
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        response["Cross-Origin-Opener-Policy"] = "same-origin"

        # Politique de sécurité du contenu (CSP)
        csp = (
            "default-src 'self'; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com data:; "
            "img-src 'self' data: blob: https://images.unsplash.com https://*.unsplash.com; "
            "script-src 'self' 'unsafe-inline'; "
            "object-src 'none';"
        )
        response["Content-Security-Policy"] = csp

        return response
