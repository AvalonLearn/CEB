from query_representation.query import *

qfn = "queries/ceb-imdb/4a/4a114.pkl"
qrep = load_qrep(qfn)

# extract basic properties of the query representation format

print("""Query has {} tables, {} joins, {} subplans.""".format(
    len(qrep["join_graph"].nodes()), len(qrep["join_graph"].edges()),
    len(qrep["subset_graph"].nodes())))

tables, aliases = get_tables(qrep)

print("Tables: ")
for i,table in enumerate(tables):
    print(table, aliases[i])

print("Joins: ")
joins = get_joins(qrep)
print(("\n").join(joins))

preds, pred_cols, pred_types, pred_vals = get_predicates(qrep)
print("Predicates: ")
for i in range(len(preds)):
    for j, pred in enumerate(preds[i]):
        print(pred.strip(" "))
        print("     Predicate column: ", pred_cols[i][j])
        print("       Predicate type: ", pred_types[i][j])
        print("     Predicate values: ", pred_vals[i][j])

qrep = load_qrep(qfn)

# for getting cardinality estimates of every subplan in the query
ests = get_postgres_cardinalities(qrep)
trues = get_true_cardinalities(qrep)

for k,v in ests.items():
    print("Subplan, joining tables: ", k)
    subsql = subplan_to_sql(qrep, k)
    print("Subplan SQL: ", subsql)
    print("   True cardinality: ", trues[k])
    print("PostgreSQL estimate: ", v)
    print("****************")