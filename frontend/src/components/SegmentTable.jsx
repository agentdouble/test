import PropTypes from 'prop-types';
import './SegmentTable.css';

function SegmentTable({ dimensionLabel, rows }) {
  if (rows.length === 0) {
    return (
      <section className="segment-table segment-table--empty">
        <p>Aucun segment disponible pour cette sélection.</p>
      </section>
    );
  }

  return (
    <section className="segment-table">
      <header className="segment-table__header">
        <h2>Performance par {dimensionLabel.toLowerCase()}</h2>
        <p>Comparez les KPIs clés par segment pour identifier les leviers de croissance.</p>
      </header>
      <div className="segment-table__scroller">
        <table>
          <thead>
            <tr>
              <th>{dimensionLabel}</th>
              <th>Revenu</th>
              <th>Commandes</th>
              <th>Leads</th>
              <th>Taux de conversion</th>
              <th>Panier moyen</th>
              <th>Revenu / Lead</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.dimension}>
                <th scope="row">{row.dimension}</th>
                <td>{row.kpis.revenue}</td>
                <td>{row.kpis.orders}</td>
                <td>{row.kpis.leads}</td>
                <td>{row.kpis.conversionRate}</td>
                <td>{row.kpis.averageOrderValue}</td>
                <td>{row.kpis.revenuePerLead}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

SegmentTable.propTypes = {
  dimensionLabel: PropTypes.string.isRequired,
  rows: PropTypes.arrayOf(
    PropTypes.shape({
      dimension: PropTypes.string.isRequired,
      kpis: PropTypes.shape({
        revenue: PropTypes.string.isRequired,
        orders: PropTypes.string.isRequired,
        leads: PropTypes.string.isRequired,
        conversionRate: PropTypes.string.isRequired,
        averageOrderValue: PropTypes.string.isRequired,
        revenuePerLead: PropTypes.string.isRequired
      }).isRequired
    })
  ).isRequired
};

export default SegmentTable;
