import { historyReducer, History, historyActionTypes } from './historyReducer';
import { List, Record } from 'immutable';

describe('historyReducer', () => {

    it('should return initial state', () => {
        expect(historyReducer(undefined, {})).toEqual(new History());
    });

    it('should handle CLEAR_HISTORY', () => {
        const init = new History({ dps: List('stuff'), data: List('things') });
        const action = { type: historyActionTypes.CLEAR_HISTORY };
        const expected = Record({ dps: List(), data: List() })();
        expect(historyReducer(init, action).equals(expected)).toBe(true);
    });

    it('should handle ADD_HISTORY', () => {
        const init = new History({ dps: [], data: [] });
        const action = {
            type: historyActionTypes.ADD_HISTORY,
            dps: 1000,
            character: { testcharcter: 'testcharcter' },
            settings: { testsetting: 'testsetting' }
        };
        const expected = new History({
            dps: [1000],
            data: [{
                character: { testcharcter: 'testcharcter' },
                settings: { testsetting: 'testsetting' }
            }]
        });
        expect(historyReducer(init, action)).toEqual(expected);
    });
});
