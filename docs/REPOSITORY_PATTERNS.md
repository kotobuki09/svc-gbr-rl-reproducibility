# Repository design rationale

This release follows patterns from established scientific software/data
projects and official repository guidance. The detailed research log is kept
with the working project; the first-party sources used for this release are
listed below so this document remains self-contained after cloning.

## Patterns adopted here

- Root README as the reviewer's route: purpose, quick start, repository map,
  data availability, reproducibility status, citation, license, and contact.
- Explicit data-availability categories: public sample, restricted source
  records, access route, terms, and affected paper outputs.
- A data card that documents schema, provenance, intended use, limitations, and
  privacy boundary without exposing restricted rows.
- A small public fixture and a default smoke test that never requires private
  files.
- `CITATION.cff`, versioned releases, and a future Zenodo DOI instead of a
  mutable “latest” citation.
- Separate code and data licenses so the code license cannot be read as a
  license for restricted operational data.
- A release audit for forbidden files, required metadata, sample provenance,
  and internal-benchmark wording.

## First-party sources consulted

- GitHub README guidance: <https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes>
- GitHub citation files: <https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files>
- GitHub releases and archival citation: <https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content>
- World Bank reproducibility checklist: <https://github.com/worldbank/wb-reproducible-research-repository/blob/main/reproducibility_package_checklist.md>
- Zenodo records and versions: <https://help.zenodo.org/docs/deposit/about-records/> and <https://help.zenodo.org/docs/deposit/manage-versions/>
- Zenodo access requests: <https://help.zenodo.org/docs/share/access-requests/>
- Google PAIR data-card guidance: <https://pair.withgoogle.com/guidebook-v2/chapter/data-collection/>
- Astropy citation and CI patterns: <https://github.com/astropy/astropy/blob/main/CITATION.cff> and <https://github.com/astropy/astropy/blob/main/docs/development/testguide.rst>
- Biopython contribution/testing patterns: <https://github.com/biopython/biopython/blob/master/CONTRIBUTING.rst>
- scikit-learn test workflow: <https://github.com/scikit-learn/scikit-learn/blob/main/.github/workflows/unit-tests.yml>

These sources informed structure and release hygiene. They do not certify the
scientific validity of the paper's internal benchmark or replace author/data-
custodian approval.
