import { useMemo, useState } from 'react';
import FilterPanel from './components/FilterPanel.jsx';
import IndicatorBuilder from './components/IndicatorBuilder.jsx';
import KpiCard from './components/KpiCard.jsx';
import SegmentTable from './components/SegmentTable.jsx';
import transactions from './data/sampleTransactions.json';
import './App.css';

const DIMENSIONS = [
  { value: 'channel', label: 'Canal' },
  { value: 'campaign', label: 'Campagne' },
  { value: 'product', label: 'Produit' }
];

const FILTER_FIELDS = DIMENSIONS;

const TABS = [
  { id: 'dashboard', label: 'Tableau de bord' },
  { id: 'indicators', label: 'Indicateurs clés' }
];

const CURRENCY_FORMATTER = new Intl.NumberFormat('fr-FR', {
  style: 'currency',
  currency: 'EUR'
});

const INTEGER_FORMATTER = new Intl.NumberFormat('fr-FR');

function computeAggregates(rows) {
  const totals = rows.reduce(
    (acc, row) => {
      acc.revenue += row.revenue;
      acc.orders += row.orders;
      acc.leads += row.leads;
      return acc;
    },
    { revenue: 0, orders: 0, leads: 0 }
  );

  const conversionRate = totals.leads === 0 ? 0 : (totals.orders / totals.leads) * 100;
  const averageOrderValue = totals.orders === 0 ? 0 : totals.revenue / totals.orders;
  const revenuePerLead = totals.leads === 0 ? 0 : totals.revenue / totals.leads;

  return {
    revenue: totals.revenue,
    orders: totals.orders,
    leads: totals.leads,
    conversionRate: Number(conversionRate.toFixed(2)),
    averageOrderValue: Number(averageOrderValue.toFixed(2)),
    revenuePerLead: Number(revenuePerLead.toFixed(2))
  };
}

function formatAggregates(aggregates) {
  return {
    revenue: CURRENCY_FORMATTER.format(aggregates.revenue),
    orders: INTEGER_FORMATTER.format(aggregates.orders),
    leads: INTEGER_FORMATTER.format(aggregates.leads),
    conversionRate: `${aggregates.conversionRate.toFixed(2)} %`,
    averageOrderValue: CURRENCY_FORMATTER.format(aggregates.averageOrderValue),
    revenuePerLead: CURRENCY_FORMATTER.format(aggregates.revenuePerLead)
  };
}

function buildFilterState() {
  return FILTER_FIELDS.reduce((state, field) => ({
    ...state,
    [field.value]: []
  }), {});
}

function App() {
  const [selectedDimension, setSelectedDimension] = useState(DIMENSIONS[0].value);
  const [filters, setFilters] = useState(buildFilterState);
  const [activeTab, setActiveTab] = useState(TABS[0].id);

  const filterOptions = useMemo(
    () =>
      FILTER_FIELDS.map((field) => ({
        field: field.value,
        label: field.label,
        values: Array.from(new Set(transactions.map((transaction) => transaction[field.value]))).sort(),
        selected: filters[field.value]
      })),
    [filters]
  );

  const filteredTransactions = useMemo(
    () =>
      transactions.filter((transaction) =>
        FILTER_FIELDS.every((field) => {
          const selectedValues = filters[field.value];
          return selectedValues.length === 0 || selectedValues.includes(transaction[field.value]);
        })
      ),
    [filters]
  );

  const aggregated = useMemo(() => computeAggregates(filteredTransactions), [filteredTransactions]);
  const formattedAggregates = useMemo(() => formatAggregates(aggregated), [aggregated]);

  const segments = useMemo(() => {
    if (!selectedDimension) {
      return [];
    }

    const groups = new Map();

    filteredTransactions.forEach((transaction) => {
      const dimensionValue = transaction[selectedDimension] ?? 'Non renseigné';
      const current = groups.get(dimensionValue) ?? [];
      current.push(transaction);
      groups.set(dimensionValue, current);
    });

    return Array.from(groups.entries())
      .map(([dimensionValue, rows]) => {
        const aggregates = computeAggregates(rows);
        return {
          dimension: dimensionValue,
          kpis: formatAggregates(aggregates),
          rawRevenue: aggregates.revenue
        };
      })
      .sort((a, b) => b.rawRevenue - a.rawRevenue)
      .map(({ rawRevenue, ...rest }) => rest);
  }, [filteredTransactions, selectedDimension]);

  const dimensionLabel = DIMENSIONS.find((dimension) => dimension.value === selectedDimension)?.label ?? 'Segment';

  const summaryCards = [
    {
      key: 'revenue',
      title: 'Revenu total',
      value: formattedAggregates.revenue,
      description: 'Somme des ventes réalisées sur la période.',
      tone: 'success'
    },
    {
      key: 'orders',
      title: 'Commandes',
      value: formattedAggregates.orders,
      description: 'Volume de commandes générées.'
    },
    {
      key: 'leads',
      title: 'Leads marketing',
      value: formattedAggregates.leads,
      description: 'Nombre de prospects capturés via vos campagnes.'
    },
    {
      key: 'conversionRate',
      title: 'Taux de conversion',
      value: formattedAggregates.conversionRate,
      description: 'Commandes / Leads.',
      tone: 'success'
    },
    {
      key: 'averageOrderValue',
      title: 'Panier moyen',
      value: formattedAggregates.averageOrderValue,
      description: 'Revenu moyen par commande.'
    },
    {
      key: 'revenuePerLead',
      title: 'Revenu par lead',
      value: formattedAggregates.revenuePerLead,
      description: 'Montant moyen généré par prospect.',
      tone: 'warning'
    }
  ];

  const handleFilterToggle = (field, value) => {
    setFilters((previous) => {
      const selection = previous[field];
      const exists = selection.includes(value);
      const updated = exists ? selection.filter((item) => item !== value) : [...selection, value];

      return {
        ...previous,
        [field]: updated
      };
    });
  };

  return (
    <div className="app">
      <header className="app__hero">
        <p className="app__badge">Plateforme ABC KPI</p>
        <h1>Visualisez vos performances marketing en temps réel</h1>
        <p className="app__subtitle">
          Analysez vos canaux d&apos;acquisition, identifiez les campagnes les plus rentables et pilotez vos revenus
          depuis un tableau de bord moderne.
        </p>
      </header>

      <nav className="app__tabs" aria-label="Sections du tableau de bord">
        {TABS.map((tab) => (
          <button
            key={tab.id}
            type="button"
            className={`app__tab ${tab.id === activeTab ? 'app__tab--active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
            aria-current={tab.id === activeTab ? 'page' : undefined}
          >
            {tab.label}
          </button>
        ))}
      </nav>

      <main className="app__content">
        {activeTab === 'indicators' ? (
          <IndicatorBuilder />
        ) : (
          <>
            <section className="app__filters">
              <FilterPanel
                dimensions={DIMENSIONS}
                selectedDimension={selectedDimension}
                onDimensionChange={setSelectedDimension}
                filters={filterOptions}
                onFilterToggle={handleFilterToggle}
              />
            </section>

            <section className="app__kpis">
              {summaryCards.map((card) => (
                <KpiCard
                  key={card.key}
                  title={card.title}
                  value={card.value}
                  description={card.description}
                  tone={card.tone}
                />
              ))}
            </section>

            <SegmentTable dimensionLabel={dimensionLabel} rows={segments} />

            <section className="app__raw-data">
              <header>
                <h2>Données transactionnelles brutes</h2>
                <p>Exportez ces données pour une analyse approfondie ou un partage dans vos outils internes.</p>
              </header>
              <div className="app__table-wrapper">
                <table>
                  <thead>
                    <tr>
                      <th>Date</th>
                      <th>Canal</th>
                      <th>Campagne</th>
                      <th>Produit</th>
                      <th>Revenu</th>
                      <th>Leads</th>
                      <th>Commandes</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredTransactions.map((transaction) => (
                      <tr key={`${transaction.date}-${transaction.campaign}-${transaction.channel}`}>
                        <td>{transaction.date}</td>
                        <td>{transaction.channel}</td>
                        <td>{transaction.campaign}</td>
                        <td>{transaction.product}</td>
                        <td>{CURRENCY_FORMATTER.format(transaction.revenue)}</td>
                        <td>{INTEGER_FORMATTER.format(transaction.leads)}</td>
                        <td>{INTEGER_FORMATTER.format(transaction.orders)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          </>
        )}
      </main>
    </div>
  );
}

export default App;
