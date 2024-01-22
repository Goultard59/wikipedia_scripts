import pywikibot
import pandas as pd

#wikidata connect
site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()

#load df
df = pd.read_csv('~/wikipedia/fr-esr-statistiques-sur-les-effectifs-d-etudiants-inscrits-par-etablissement-hcp.csv', sep=";")
df = df[df['etablissement_id_wikidata'].notna()]

#np.where(df['etablissement_id_wikidata'].unique() == "Q80186910")

for wikidataid in df['etablissement_id_wikidata'].unique()[150:]:
  df_etablissement = df[df['etablissement_id_wikidata'] == wikidataid]
  for year in df_etablissement['annee'].unique():
    # source
    statedin = pywikibot.Claim(repo, 'P248')
    itis = pywikibot.ItemPage(repo, "Q3016893")
    statedin.setTarget(itis)
    #source url
    urlref = pywikibot.Claim(repo, 'P854')
    urlref.setTarget("https://data.enseignementsup-recherche.gouv.fr/explore/dataset/fr-esr-statistiques-sur-les-effectifs-d-etudiants-inscrits-par-etablissement-hcp/table/?sort=-annee_universitaire")
    #source author
    author = pywikibot.Claim(repo, 'P50')
    itis = pywikibot.ItemPage(repo, "Q2726949")
    author.setTarget(itis)
    #source date
    retrieved = pywikibot.Claim(repo, 'P813')
    date = pywikibot.WbTime(year=2023, month=12, day=15)
    retrieved.setTarget(date)
    #end source
    effectif_eleve = df_etablissement.loc[df_etablissement['annee'] == year, 'effectif'].iloc[0]
    print(wikidataid)
    print(year)
    #page id
    item = pywikibot.ItemPage(repo, wikidataid)
    #ajout value
    claim = pywikibot.Claim(repo, 'P2196')
    target = pywikibot.WbQuantity(effectif_eleve)
    #ajout year
    qualifier = pywikibot.Claim(repo, 'P585')
    current_year = pywikibot.WbTime(year=year)
    qualifier.setTarget(current_year)
    claim.setTarget(target)
    claim.addQualifier(qualifier, summary='Adding a qualifier.')
    claim.addSources([statedin, urlref, author, retrieved], summary='Adding sources.')
    item.addClaim(claim, summary='Script add student number per year')
    del claim