import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';

import RankingSection from '../SidebarRanking';
import TalentFrame from './TalentFrame';
import * as layouts from './TalentLayouts';
import store from '../store';
import { changeSpecialization } from '../store';

function TalentSetButton(props) {
    return (
        <button className="talent_set ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only" data-spec={props.spec} data-talents={props.talents} role="button" onClick={props.handler}>
            <span className="ui-button-text">{props.name}</span>
        </button>
    );
}

TalentSetButton.propTypes = {
    spec: PropTypes.string.isRequired,
    talents: PropTypes.string.isRequired,
    handler: PropTypes.func.isRequired,
    name: PropTypes.string.isRequired
};

class TalentPane extends React.Component {

    constructor(props) {
        super(props);
        this.clickButton = this.clickButton.bind(this);
    }

    componentDidMount() {
        // This is a bit of a hack and is probably a bit fragile depending on if wowdb ever
        // changes any of this, but it rescans the DOM for elements that should display a
        // tooltip.
        CurseTips['wowdb-tooltip'].watchElligibleElements();
    }

    clickButton(e) {
        e.preventDefault();
        store.dispatch(changeSpecialization(
            this.props.activeSpec,
            e.currentTarget.dataset.spec,
            e.currentTarget.dataset.talents
        ));
    }

    render() {
        var frame = null;
        var ranking_frame = null;

        if (this.props.activeSpec == 'a') {
            frame = <TalentFrame layout={layouts.assassination_layout} />;
            ranking_frame = <RankingSection id="talentrankings" name="Talent Rankings" layout={layouts.assassination_ranking} values={this.props.rankings} />;
        }
        else if (this.props.activeSpec == 'Z') {
            frame = <TalentFrame layout={layouts.outlaw_layout} />;
            ranking_frame = <RankingSection id="talentrankings" name="Talent Rankings" layout={layouts.outlaw_ranking} values={this.props.rankings} />;
        }
        else if (this.props.activeSpec == 'b') {
            frame = <TalentFrame layout={layouts.subtlety_layout} />;
            ranking_frame = <RankingSection id="talentrankings" name="Talent Rankings" layout={layouts.subtlety_ranking} values={this.props.rankings} />;
        }

        return (
            <div className="with-tools ui-tabs-panel ui-widget-content ui-corner-bottom ui-tabs-hide" id="talents">
                <div className="panel-tools">
                    <section>
                        <h3>Talent Sets</h3>
                        <div className="inner" id="talentsets">
                            <TalentSetButton spec="a" talents={this.props.talents.get('a')} name="Imported Assassination" handler={this.clickButton} />
                            <TalentSetButton spec="Z" talents={this.props.talents.get('Z')} name="Imported Outlaw" handler={this.clickButton} />
                            <TalentSetButton spec="b" talents={this.props.talents.get('b')} name="Imported Subtlety" handler={this.clickButton} />
                            <TalentSetButton spec="a" talents="2211021" name="Stock Assassination" handler={this.clickButton} />
                            <TalentSetButton spec="Z" talents="2211011" name="Stock Outlaw" handler={this.clickButton} />
                            <TalentSetButton spec="b" talents="1210011" name="Stock Subtlety" handler={this.clickButton} />
                        </div>
                    </section>
                    {ranking_frame}
                </div>
                {frame}
            </div>
        );
    }
}

TalentPane.propTypes = {
    activeSpec: PropTypes.string.isRequired,
    rankings: PropTypes.object.isRequired,
    talents: PropTypes.object.isRequired
};

const mapStateToProps = function (store) {
    return {
        rankings: store.engine.talentRanking,
        activeSpec: store.character.get('active'),
        talents: store.character.get('talents')
    };
};

export default connect(mapStateToProps)(TalentPane);
