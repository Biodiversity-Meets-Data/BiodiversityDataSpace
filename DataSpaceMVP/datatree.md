This is based on the WP3 data cube in netcdf 
Link: https://github.com/nbillietPM/BmC/tree/main

```
============================================================
DATATREE NETCDF FILE INVESTIGATION
============================================================

DataTree structure:
DataTree('None', parent=None)
├── DataTree('static')
│   ├── DataTree('chelsa_clim_ref_period')
│   │       Dimensions:  (lat: 23, long: 69)
│   │       Coordinates:
│   │         * lat      (lat) float64 184B 50.87 50.87 50.86 50.85 ... 50.71 50.7 50.69
│   │         * long     (long) float64 552B 4.176 4.184 4.192 4.201 ... 4.726 4.734 4.742
│   │       Data variables:
│   │           bio1     (lat, long) uint16 3kB ...
│   │           bio2     (lat, long) uint16 3kB ...
│   │           bio3     (lat, long) float32 6kB ...
│   ├── DataTree('chelsa_clim_ref_month')
│   │       Dimensions:  (months: 2, lat: 23, long: 69)
│   │       Coordinates:
│   │         * months   (months) int64 16B 1 2
│   │         * lat      (lat) float64 184B 50.87 50.87 50.86 50.85 ... 50.71 50.7 50.69
│   │         * long     (long) float64 552B 4.176 4.184 4.192 4.201 ... 4.726 4.734 4.742
│   │       Data variables:
│   │           tas      (months, lat, long) float64 25kB ...
│   │           tasmin   (months, lat, long) uint16 6kB ...
│   │           tasmax   (months, lat, long) uint16 6kB ...
│   ├── DataTree('chelsa_clim_sim_period')
│   │       Dimensions:          (year_range: 2, model_name: 1, ensemble_member: 2,
│   │                             lat: 23, long: 69)
│   │       Coordinates:
│   │         * year_range       (year_range) <U9 72B '2011-2040' '2041-2070'
│   │         * model_name       (model_name) <U9 36B 'gfdl-esm4'
│   │         * ensemble_member  (ensemble_member) <U6 48B 'ssp370' 'ssp126'
│   │         * lat              (lat) float64 184B 50.87 50.87 50.86 ... 50.71 50.7 50.69
│   │         * long             (long) float64 552B 4.176 4.184 4.192 ... 4.726 4.734 4.742
│   │       Data variables:
│   │           bio1             (year_range, model_name, ensemble_member, lat, long) uint16 13kB ...
│   │           bio2             (year_range, model_name, ensemble_member, lat, long) uint16 13kB ...
│   │           bio3             (year_range, model_name, ensemble_member, lat, long) float32 25kB ...
│   └── DataTree('chelsa_clim_sim_month')
│           Dimensions:          (year_range: 2, month: 1, model_name: 1,
│                                 ensemble_member: 2, lat: 23, long: 69)
│           Coordinates:
│             * year_range       (year_range) <U9 72B '2011-2040' '2041-2070'
│             * month            (month) int64 8B 1
│             * model_name       (model_name) <U12 48B 'ipsl-cm6a-lr'
│             * ensemble_member  (ensemble_member) <U6 48B 'ssp585' 'ssp126'
│             * lat              (lat) float64 184B 50.87 50.87 50.86 ... 50.71 50.7 50.69
│             * long             (long) float64 552B 4.176 4.184 4.192 ... 4.726 4.734 4.742
│           Data variables:
│               tas              (year_range, month, model_name, ensemble_member, lat, long) uint16 13kB ...
│               tasmin           (year_range, month, model_name, ensemble_member, lat, long) uint16 13kB ...
│               tasmax           (year_range, month, model_name, ensemble_member, lat, long) uint16 13kB ...
└── DataTree('dynamic')
    ├── DataTree('chelsa_month')
    │       Dimensions:  (time: 2, lat: 23, long: 69)
    │       Coordinates:
    │         * time     (time) datetime64[ns] 16B 1980-01-01 1980-02-01
    │         * lat      (lat) float64 184B 50.87 50.87 50.86 50.85 ... 50.71 50.7 50.69
    │         * long     (long) float64 552B 4.176 4.184 4.192 4.201 ... 4.726 4.734 4.742
    │       Data variables:
    │           tas      (time, lat, long) float64 25kB ...
    │           tasmin   (time, lat, long) int32 13kB ...
    │           tasmax   (time, lat, long) int32 13kB ...
    └── DataTree('gbif_occurences')
            Dimensions:      (ndim: 6, nnz: 99549, specieskey: 140, genuskey: 110,
                              familykey: 60, classkey: 8, eeacellcode: 1047, time: 488)
            Coordinates:
              * specieskey   (specieskey) int64 1kB 2432427 2432452 ... 9752617 11071158
              * genuskey     (genuskey) int64 880B 2432384 2475493 ... 10792217 11086674
              * familykey    (familykey) int64 480B 2407 2410 2416 ... 4408414 6101019
              * classkey     (classkey) float64 64B 194.0 196.0 212.0 ... 359.0 7.229e+06
              * eeacellcode  (eeacellcode) <U13 54kB '1kmE3907N3097' ... '1kmE3954N3100'
              * time         (time) datetime64[ns] 4kB 1980-01-01 1980-02-01 ... 2020-12-01
            Dimensions without coordinates: ndim, nnz
            Data variables:
                coords       (ndim, nnz) int16 1MB ...
                data         (nnz) int64 796kB ...
                shape        (ndim) int64 48B ...
                dims         (ndim) <U11 264B ...
            Attributes:
                __orig_var_name__:  occurrences

============================================================
EXPLORING NODES/GROUPS
============================================================

/
----------------------------------------

/static/
----------------------------------------

/static/chelsa_clim_ref_period/
----------------------------------------
Data variables:
  bio1: (23, 69) ('lat', 'long')
  bio2: (23, 69) ('lat', 'long')
  bio3: (23, 69) ('lat', 'long')
Coordinates:
  lat: (23,) ('lat',)
  long: (69,) ('long',)

/static/chelsa_clim_ref_month/
----------------------------------------
Data variables:
  tas: (2, 23, 69) ('months', 'lat', 'long')
  tasmin: (2, 23, 69) ('months', 'lat', 'long')
  tasmax: (2, 23, 69) ('months', 'lat', 'long')
Coordinates:
  months: (2,) ('months',)
  lat: (23,) ('lat',)
  long: (69,) ('long',)

/static/chelsa_clim_sim_period/
----------------------------------------
Data variables:
  bio1: (2, 1, 2, 23, 69) ('year_range', 'model_name', 'ensemble_member', 'lat', 'long')
  bio2: (2, 1, 2, 23, 69) ('year_range', 'model_name', 'ensemble_member', 'lat', 'long')
  bio3: (2, 1, 2, 23, 69) ('year_range', 'model_name', 'ensemble_member', 'lat', 'long')
Coordinates:
  year_range: (2,) ('year_range',)
  model_name: (1,) ('model_name',)
  ensemble_member: (2,) ('ensemble_member',)
  lat: (23,) ('lat',)
  long: (69,) ('long',)

/static/chelsa_clim_sim_month/
----------------------------------------
Data variables:
  tas: (2, 1, 1, 2, 23, 69) ('year_range', 'month', 'model_name', 'ensemble_member', 'lat', 'long')
  tasmin: (2, 1, 1, 2, 23, 69) ('year_range', 'month', 'model_name', 'ensemble_member', 'lat', 'long')
  tasmax: (2, 1, 1, 2, 23, 69) ('year_range', 'month', 'model_name', 'ensemble_member', 'lat', 'long')
Coordinates:
  year_range: (2,) ('year_range',)
  month: (1,) ('month',)
  model_name: (1,) ('model_name',)
  ensemble_member: (2,) ('ensemble_member',)
  lat: (23,) ('lat',)
  long: (69,) ('long',)

/dynamic/
----------------------------------------

/dynamic/chelsa_month/
----------------------------------------
Data variables:
  tas: (2, 23, 69) ('time', 'lat', 'long')
  tasmin: (2, 23, 69) ('time', 'lat', 'long')
  tasmax: (2, 23, 69) ('time', 'lat', 'long')
Coordinates:
  time: (2,) ('time',)
  lat: (23,) ('lat',)
  long: (69,) ('long',)

/dynamic/gbif_occurences/
----------------------------------------
Data variables:
  coords: (6, 99549) ('ndim', 'nnz')
  data: (99549,) ('nnz',)
  shape: (6,) ('ndim',)
  dims: (6,) ('ndim',)
Coordinates:
  specieskey: (140,) ('specieskey',)
  genuskey: (110,) ('genuskey',)
  familykey: (60,) ('familykey',)
  classkey: (8,) ('classkey',)
  eeacellcode: (1047,) ('eeacellcode',)
  time: (488,) ('time',)

============================================================
```
