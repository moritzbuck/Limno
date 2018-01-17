from random import choices, choice, uniform, normalvariate
from numpy import mean, log10

BASES = ['A','T','C','G']

class Gene:

    def __init__(self, length_gene, mutation_rate, functional_cutoff):
        self.seq = "".join(choices(BASES, k=length_gene))
        self.mutation_rate = mutation_rate
        self.functional_cutoff = functional_cutoff

    def mutate(self):
        self.seq = "".join([s if uniform(0,1) > r else choice(list(set(BASES).difference(s))) for s in seq])

    def copy(self):
        out = Gene(len(self.seq), self.mutation_rate, self.functional_cutoff)
        out.seq = self.seq
        return out

class Model:

    __init__(self, type, min_mut = None, max_mut = None, functional_cutoff = None, var_functional_cutoff = None):
        self.functional_cutoffs = lambda nb_genes : [normalvariate(functional_cutoff,var_functional_cutoff) for g in range(nb_genes)]
        self.mutation_rates = lambda nb_genes : [10**-uniform(log10(min_mut),log10(max_mut)) for g in range(nb_genes)]



class Genome:

    mutate = lambda seq, r : "".join([s if uniform(0,1) > r else choice(list(set(BASES).difference(s))) for s in seq])
    simi = lambda a,b : sum([x == y for x,y in zip(a,b)])/len(a)

    def __init__(self, nb_genes, length_genes, model = None):
        if model:
            mutation_rates = model.mutation_rates(nb_genes)
            functional_cutoffs = model.functional_cutoffs(nb_genes)
        else:
            mutation_rates = [0.001]*nb_genes
            functional_cutoffs = [0.7]*nb_genes

        self.genome = [Gene(length_genes) for i,m,f in zip(range(nb_genes), mutation_rates, functional_cutoffs)]

    def copy(self):
        out_genome = Genome(1,1)
        out_genome.genome = self.genome


        cutoffs = [normalvariate(0.5,0.15) for g in genome]
        var_muts = [10**-uniform(3,6) for g in genome]
        func_cutof =  mean(cutoffs)
reps = 100000
mut_rate = mean(var_muts)

ori_genome = genome

outp =["gen\tseq_id\tfunct_id\tmodel\n"]

for i in range(reps):
    print(i)
    genome = [mutate(s,mut) for s,mut in zip(genome,var_muts)]
    simis = [simi(g1,g2) for g1,g2 in zip(ori_genome, genome)]
    seq_id = mean(simis)
    funct_id = str(sum([s > func_cutof for s in simis])/ len(simis))
    if i%10 == 0:
        outp.append("{i}\t{seq}\t{funct}\tvarmuts\n".format(i=i, seq=seq_id, funct=funct_id) )

genome = ori_genome

for i in range(reps):
    print(i)
    genome = [mutate(s,mut_rate) for s in genome]
    simis = [simi(g1,g2) for g1,g2 in zip(ori_genome, genome)]
    seq_id = mean(simis)
    funct_id = str(sum([s > c for s,c in zip(simis,cutoffs)])/ len(simis))
    if i%10 == 0:
        outp.append("{i}\t{seq}\t{funct}\tvarcutoff\n".format(i=i, seq=seq_id, funct=funct_id) )

genome = ori_genome
for i in range(reps):
    print(i)
    genome = [mutate(s,mut_rate) for s in genome]
    simis = [simi(g1,g2) for g1,g2 in zip(ori_genome, genome)]
    seq_id = mean(simis)
    funct_id = str(sum([s > func_cutof for s in simis])/ len(simis))
    if i%10 == 0:
        outp.append("{i}\t{seq}\t{funct}\tdrift\n".format(i=i, seq=seq_id, funct=funct_id))

genome = ori_genome

for i in range(reps):
    print(i)
    genome = [mutate(s,mut) for s,mut in zip(genome,var_muts)]
    simis = [simi(g1,g2) for g1,g2 in zip(ori_genome, genome)]
    seq_id = mean(simis)
    funct_id = str(sum([s > c for s,c in zip(simis,cutoffs)])/ len(simis))
    if i%10 == 0:
        outp.append("{i}\t{seq}\t{funct}\tvarboth\n".format(i=i, seq=seq_id, funct=funct_id) )



with open("out.tsv","w") as handle:
    handle.writelines(outp)
