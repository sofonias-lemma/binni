# Binyam House 3D viewer

Interactive 3D model of the Ato Biniyam G+4 house, published with GitHub Pages.

Live site (once Pages is switched on): https://sofonias-lemma.github.io/binni/

## Layout

- `site/index.html` – the viewer page (three.js, loaded from the jsDelivr CDN)
- `site/binyam_house.glb` – the house model, loaded by the page with a relative URL
- `tools/build_site.py` – rebuilds `site/` from the project's `house3d.html`
- `.github/workflows/pages.yml` – deploys `site/` to Pages on every push to `main`

## Updating the model

The viewer in the project folder (`drawings/3d/house3d.html`) embeds the model.
After it changes, rebuild and commit:

```
python3 tools/build_site.py path/to/house3d.html
git add site && git commit -m "Update 3D viewer" && git push
```

The script splits the embedded model out into `site/binyam_house.glb`.
