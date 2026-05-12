# Dossier Images - CSECJF

Ce dossier contient toutes les images du site web du Centre Socio-Éducatif et Culturel des Jeunes et Femmes (CSECJF) de Guinaw Rails Sud.

## Structure des dossiers

| Dossier | Contenu |
|---------|---------|
| `accueil/` | Images de la page d'accueil (hero, présentation) |
| `about/` | Images de la page À Propos (bâtiment, maire, équipe dirigeante) |
| `services/` | Images de la page Services (BEL, formation, salles) |
| `achievements/` | Images de la page Réalisations (projets, témoignages) |
| `shared/` | Images communes à plusieurs pages (logo, favicon, icônes) |

## Comment utiliser les images dans le HTML

Remplacez les URLs externes par des chemins relatifs comme suit :

```html
<!-- Avant -->
<img src="https://lh3.googleusercontent.com/aida-public/..." alt="Description">

<!-- Après -->
<img src="image/accueil/hero.jpg" alt="Description">
```

## Conseils de nommage

- Utilisez des noms descriptifs en minuscules (ex: `hero-accueil.jpg`, `equipe-directrice.jpg`)
- Évitez les espaces et caractères spéciaux
- Préférez les formats WebP, JPG ou PNG

