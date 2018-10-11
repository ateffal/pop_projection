# pop_projection

Projection of a population consisting of :

actives
retirees
their conjoints
thier children
widows
orphans
Given such population at year 0, we compute, for each following year (year 1, year 2, ..., year 100, and at the end of that year), the number of individuals, that survived, died and quit the company (actives only) and those that retired (actives only). In addition to that, new children, new conjoints, and new actives are also generated using given laws.

The laws governing suchs movements are :

law of mortality
law of quitting
law of retirement (this one is in fact deterministic : retirement at some age , 60 for example)
law of birth
law of marriage
We'll began with simple laws that depends on age only. But I hope to extend it to law with arbitray parameters. For example, law of mortality my depend on age, sexe and year of projection.

The main function of this package (simulerEffectif) may return a (n_individuals * n_years) matrix of numbers (one number for each individual and each year) for each of the above sub populations.
