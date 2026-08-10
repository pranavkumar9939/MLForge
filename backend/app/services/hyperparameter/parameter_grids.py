from sklearn.svm import SVR, SVC
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier,DecisionTreeRegressor
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor

PARAMETER_GRIDS = {

    "Random Forest": {

        "n_estimators": [100, 200, 300],

        "max_depth": [
            None,
            10,
            20,
            30
        ],

        "min_samples_split": [
            2,
            5,
            10
        ]
    },

    "Decision Tree": {

        "max_depth": [
            None,
            5,
            10,
            20
        ],

        "min_samples_split": [
            2,
            5,
            10
        ]
    },

    "SVM": {

        "C": [
            0.1,
            1,
            10,
            100
        ],

        "gamma": [
            "scale",
            "auto"
        ],

        "kernel": [
            "rbf",
            "linear"
        ]
    },

    "KNN": {

        "n_neighbors": [
            3,
            5,
            7,
            9
        ],

        "weights": [
            "uniform",
            "distance"
        ]
    },

    "Random Forest Regressor": {

        "n_estimators": [
            100,
            200,
            300
        ],

        "max_depth": [
            None,
            10,
            20
        ]
    },

    "Decision Tree Regressor": {

        "max_depth": [
            None,
            5,
            10,
            20
        ]
    },

    "SVR": {

        "C": [
            0.1,
            1,
            10
        ],

        "kernel": [
            "rbf",
            "linear"
        ]
    },

    "KNN Regressor": {

        "n_neighbors": [
            3,
            5,
            7,
            9
        ]
    }
}