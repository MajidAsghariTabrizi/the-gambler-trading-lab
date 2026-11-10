# Scientific archiving assessment (2026-11-09)

## Eligibility
- Zenodo (GitHub release archival, versioned DOI): ELIGIBLE via owner's connected account. This repo already uses GitHub Releases; Zenodo can mint a DOI per release tag automatically once the owner enables the repository on zenodo.org and authorizes the GitHub link. NO fake DOI is generated here.
- arXiv: NOT_RELEVANT now - the work is an engineering case study, not formatted for arXiv sections; no endorsement pipeline. Revisit only if the owner wants a reformatted preprint.
- Software Heritage: automatically crawls GitHub public repos - no action required; noted as passive preservation.

## Prepared submission package
- CITATION.cff updated (v2.0.0, preferred-citation = the paper).
- Release v2.0.0 notes reference the paper, canonical URL, evidence manifest hashes, and the claims table.

## Blocker
- DOI_STATUS: BLOCKED_AUTH - creating the Zenodo record requires the owner's Zenodo account authorization. Everything else is staged.
