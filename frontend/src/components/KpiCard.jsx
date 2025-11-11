import PropTypes from 'prop-types';
import './KpiCard.css';

function KpiCard({ title, value, description, tone = 'default' }) {
  return (
    <article className={`kpi-card kpi-card--${tone}`}>
      <header className="kpi-card__header">
        <p className="kpi-card__title">{title}</p>
        <p className="kpi-card__description">{description}</p>
      </header>
      <p className="kpi-card__value">{value}</p>
    </article>
  );
}

KpiCard.propTypes = {
  title: PropTypes.string.isRequired,
  value: PropTypes.string.isRequired,
  description: PropTypes.string.isRequired,
  tone: PropTypes.oneOf(['default', 'success', 'warning'])
};

export default KpiCard;
