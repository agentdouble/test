import PropTypes from 'prop-types';
import './FilterPanel.css';

function FilterPanel({
  dimensions,
  selectedDimension,
  onDimensionChange,
  filters,
  onFilterToggle
}) {
  return (
    <section className="filter-panel">
      <div className="filter-panel__group">
        <label htmlFor="dimension" className="filter-panel__label">
          Dimension d'analyse
        </label>
        <select
          id="dimension"
          className="filter-panel__select"
          value={selectedDimension}
          onChange={(event) => onDimensionChange(event.target.value)}
        >
          {dimensions.map((dimension) => (
            <option key={dimension.value} value={dimension.value}>
              {dimension.label}
            </option>
          ))}
        </select>
      </div>
      <div className="filter-panel__filters">
        {filters.map((filter) => (
          <fieldset key={filter.field} className="filter-panel__fieldset">
            <legend>{filter.label}</legend>
            <div className="filter-panel__options">
              {filter.values.map((value) => (
                <label key={value} className="filter-panel__option">
                  <input
                    type="checkbox"
                    checked={filter.selected.includes(value)}
                    onChange={() => onFilterToggle(filter.field, value)}
                  />
                  <span>{value}</span>
                </label>
              ))}
              {filter.values.length === 0 && (
                <p className="filter-panel__empty">Aucune donnée disponible</p>
              )}
            </div>
          </fieldset>
        ))}
      </div>
    </section>
  );
}

FilterPanel.propTypes = {
  dimensions: PropTypes.arrayOf(
    PropTypes.shape({
      label: PropTypes.string.isRequired,
      value: PropTypes.string.isRequired
    })
  ).isRequired,
  selectedDimension: PropTypes.string.isRequired,
  onDimensionChange: PropTypes.func.isRequired,
  filters: PropTypes.arrayOf(
    PropTypes.shape({
      field: PropTypes.string.isRequired,
      label: PropTypes.string.isRequired,
      values: PropTypes.arrayOf(PropTypes.string).isRequired,
      selected: PropTypes.arrayOf(PropTypes.string).isRequired
    })
  ).isRequired,
  onFilterToggle: PropTypes.func.isRequired
};

export default FilterPanel;
