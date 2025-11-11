import { useMemo, useState } from 'react';
import './IndicatorBuilder.css';

const UNIT_OPTIONS = [
  { value: '€', label: 'Euro (€)' },
  { value: '%', label: 'Pourcentage (%)' },
  { value: 'nb', label: 'Nombre' }
];

const DIRECTION_OPTIONS = [
  { value: 'ascending', label: 'Croissant', description: 'Plus la valeur est élevée, mieux c\'est.' },
  { value: 'descending', label: 'Décroissant', description: 'Plus la valeur est faible, mieux c\'est.' }
];

const FREQUENCY_OPTIONS = [
  { value: 'daily', label: 'Journalier' },
  { value: 'weekly', label: 'Hebdomadaire' },
  { value: 'monthly', label: 'Mensuel' },
  { value: 'quarterly', label: 'Trimestriel' },
  { value: 'yearly', label: 'Annuel' }
];

const SECTION_OPTIONS = [
  { value: 'acquisition', label: 'Acquisition' },
  { value: 'activation', label: 'Activation' },
  { value: 'retention', label: 'Rétention' },
  { value: 'revenue', label: 'Revenus' }
];

const SOURCE_OPTIONS = [
  { value: 'revenue', label: 'Revenu total' },
  { value: 'orders', label: 'Commandes' },
  { value: 'leads', label: 'Leads marketing' },
  { value: 'conversionRate', label: 'Taux de conversion' },
  { value: 'averageOrderValue', label: 'Panier moyen' },
  { value: 'revenuePerLead', label: 'Revenu par lead' }
];

const createDefaultForm = () => ({
  name: '',
  description: '',
  unit: UNIT_OPTIONS[0].value,
  direction: DIRECTION_OPTIONS[0].value,
  tolerance: 5,
  frequency: FREQUENCY_OPTIONS[1].value,
  section: SECTION_OPTIONS[0].value,
  source: SOURCE_OPTIONS[0].value
});

function IndicatorBuilder() {
  const [form, setForm] = useState(createDefaultForm);
  const [indicators, setIndicators] = useState([]);
  const [errors, setErrors] = useState({});

  const directionCopy = useMemo(
    () =>
      DIRECTION_OPTIONS.find((option) => option.value === form.direction)?.description ??
      "Définissez si l'objectif doit augmenter ou diminuer.",
    [form.direction]
  );

  const sourceLabel = useMemo(
    () => SOURCE_OPTIONS.find((option) => option.value === form.source)?.label ?? 'Indicateur lié',
    [form.source]
  );

  const sectionLabel = useMemo(
    () => SECTION_OPTIONS.find((option) => option.value === form.section)?.label ?? 'Section',
    [form.section]
  );

  const toleranceSummary = useMemo(() => {
    if (form.unit === '%') {
      return `${form.tolerance} points de ${form.unit}`;
    }
    if (form.unit === '€') {
      return `${form.tolerance} ${form.unit}`;
    }
    return `${form.tolerance} ${form.unit === 'nb' ? 'unités' : ''}`;
  }, [form.tolerance, form.unit]);

  const preview = useMemo(
    () => ({
      name: form.name || 'Nom de l\'indicateur',
      description:
        form.description ||
        "Ajoutez une description pour contextualiser l\'indicateur auprès de vos équipes.",
      details: [
        `${sourceLabel} suivis en ${UNIT_OPTIONS.find((unit) => unit.value === form.unit)?.label}.`,
        `Période d'analyse : ${FREQUENCY_OPTIONS.find((frequency) => frequency.value === form.frequency)?.label}.`,
        `${directionCopy} Tolérance de ${toleranceSummary}.`,
        `Organisé dans la section "${sectionLabel}".`
      ]
    }),
    [directionCopy, form.description, form.frequency, form.name, form.unit, sectionLabel, sourceLabel, toleranceSummary]
  );

  const handleChange = (field, value) => {
    setForm((previous) => ({
      ...previous,
      [field]: value
    }));
    setErrors((previous) => ({
      ...previous,
      [field]: undefined
    }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    const nextErrors = {};
    if (!form.name.trim()) {
      nextErrors.name = "Donnez un nom à l'indicateur";
    }

    if (Object.keys(nextErrors).length > 0) {
      setErrors(nextErrors);
      return;
    }

    const newIndicator = {
      ...form,
      id: `${form.name}-${Date.now()}`
    };

    setIndicators((previous) => [newIndicator, ...previous]);
    setForm(createDefaultForm());
  };

  const handleReset = () => {
    setForm(createDefaultForm());
    setErrors({});
  };

  const handleRemove = (id) => {
    setIndicators((previous) => previous.filter((indicator) => indicator.id !== id));
  };

  return (
    <section className="indicator-builder">
      <div className="indicator-builder__intro">
        <span className="indicator-builder__tag">Indicateurs personnalisés</span>
        <h2>Créez vos indicateurs clés en quelques clics</h2>
        <p>
          Définissez le nom, l'unité, le sens de variation et la tolérance de vos KPI. Choisissez la fréquence de
          suivi, liez-les à vos sections métier et partagez une description pour aligner vos équipes.
        </p>
      </div>

      <div className="indicator-builder__layout">
        <form className="indicator-builder__form" onSubmit={handleSubmit}>
          <div className="indicator-builder__field">
            <label htmlFor="indicator-name">Nom de l'indicateur</label>
            <input
              id="indicator-name"
              type="text"
              placeholder="Ex: Taux de transformation site"
              value={form.name}
              onChange={(event) => handleChange('name', event.target.value)}
              className={errors.name ? 'indicator-builder__input--error' : ''}
            />
            {errors.name && <span className="indicator-builder__error">{errors.name}</span>}
          </div>

          <div className="indicator-builder__grid">
            <div className="indicator-builder__field">
              <label htmlFor="indicator-unit">Unité</label>
              <select
                id="indicator-unit"
                value={form.unit}
                onChange={(event) => handleChange('unit', event.target.value)}
              >
                {UNIT_OPTIONS.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>

            <div className="indicator-builder__field">
              <label htmlFor="indicator-frequency">Fréquence de suivi</label>
              <select
                id="indicator-frequency"
                value={form.frequency}
                onChange={(event) => handleChange('frequency', event.target.value)}
              >
                {FREQUENCY_OPTIONS.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <fieldset className="indicator-builder__field">
            <legend>Sens de variation</legend>
            <div className="indicator-builder__toggle">
              {DIRECTION_OPTIONS.map((option) => {
                const isActive = option.value === form.direction;
                return (
                  <button
                    type="button"
                    key={option.value}
                    onClick={() => handleChange('direction', option.value)}
                    className={isActive ? 'is-active' : ''}
                  >
                    {option.label}
                  </button>
                );
              })}
            </div>
            <p className="indicator-builder__helper">{directionCopy}</p>
          </fieldset>

          <div className="indicator-builder__field">
            <label htmlFor="indicator-tolerance">
              Tolérance ({toleranceSummary})
            </label>
            <input
              id="indicator-tolerance"
              type="range"
              min="0"
              max="50"
              step="1"
              value={form.tolerance}
              onChange={(event) => handleChange('tolerance', Number(event.target.value))}
            />
          </div>

          <div className="indicator-builder__field">
            <label htmlFor="indicator-section">Section métier</label>
            <select
              id="indicator-section"
              value={form.section}
              onChange={(event) => handleChange('section', event.target.value)}
            >
              {SECTION_OPTIONS.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>

          <div className="indicator-builder__field">
            <label htmlFor="indicator-source">Donnée associée</label>
            <select
              id="indicator-source"
              value={form.source}
              onChange={(event) => handleChange('source', event.target.value)}
            >
              {SOURCE_OPTIONS.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>

          <div className="indicator-builder__field">
            <label htmlFor="indicator-description">Description</label>
            <textarea
              id="indicator-description"
              rows="3"
              placeholder="Ajoutez un contexte ou la formule de calcul pour vos équipes."
              value={form.description}
              onChange={(event) => handleChange('description', event.target.value)}
            />
          </div>

          <div className="indicator-builder__actions">
            <button type="submit">Enregistrer l'indicateur</button>
            <button type="button" onClick={handleReset} className="secondary">
              Réinitialiser
            </button>
          </div>
        </form>

        <aside className="indicator-builder__preview">
          <h3>Prévisualisation</h3>
          <article>
            <header>
              <h4>{preview.name}</h4>
              <span className="indicator-builder__badge">{sourceLabel}</span>
            </header>
            <p>{preview.description}</p>
            <ul>
              {preview.details.map((item, index) => (
                <li key={index}>{item}</li>
              ))}
            </ul>
          </article>
        </aside>
      </div>

      {indicators.length > 0 && (
        <div className="indicator-builder__list">
          <h3>Indicateurs enregistrés</h3>
          <ul>
            {indicators.map((indicator) => (
              <li key={indicator.id}>
                <div>
                  <h4>{indicator.name}</h4>
                  <p>{indicator.description || 'Aucune description fournie.'}</p>
                  <dl>
                    <div>
                      <dt>Unité</dt>
                      <dd>{UNIT_OPTIONS.find((option) => option.value === indicator.unit)?.label}</dd>
                    </div>
                    <div>
                      <dt>Variation</dt>
                      <dd>
                        {DIRECTION_OPTIONS.find((option) => option.value === indicator.direction)?.label} - Tolérance :{' '}
                        {indicator.tolerance} {indicator.unit === 'nb' ? 'unités' : indicator.unit}
                      </dd>
                    </div>
                    <div>
                      <dt>Fréquence</dt>
                      <dd>{FREQUENCY_OPTIONS.find((option) => option.value === indicator.frequency)?.label}</dd>
                    </div>
                    <div>
                      <dt>Section</dt>
                      <dd>{SECTION_OPTIONS.find((option) => option.value === indicator.section)?.label}</dd>
                    </div>
                    <div>
                      <dt>Donnée</dt>
                      <dd>{SOURCE_OPTIONS.find((option) => option.value === indicator.source)?.label}</dd>
                    </div>
                  </dl>
                </div>
                <button type="button" onClick={() => handleRemove(indicator.id)}>
                  Retirer
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </section>
  );
}

export default IndicatorBuilder;
