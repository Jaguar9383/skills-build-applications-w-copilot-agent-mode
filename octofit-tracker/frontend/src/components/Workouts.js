import React, { useState, useEffect } from 'react';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/workouts/`;

  useEffect(() => {
    console.log('Workouts component - API endpoint:', API_URL);
    
    fetch(API_URL)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Workouts component - Fetched data:', data);
        // Handle both paginated (.results) and plain array responses
        const workoutsData = data.results || data;
        setWorkouts(Array.isArray(workoutsData) ? workoutsData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Workouts component - Error fetching data:', error);
        setError(error.message);
        setLoading(false);
      });
  }, [API_URL]);

  if (loading) return <div className="container mt-4"><div className="alert alert-info">Loading workouts...</div></div>;
  if (error) return <div className="container mt-4"><div className="alert alert-danger">Error: {error}</div></div>;

  return (
    <div className="container mt-4">
      <h2 className="mb-4">Workout Suggestions</h2>
      <div className="row">
        {workouts.length === 0 ? (
          <div className="col-12">
            <div className="alert alert-warning">No workout suggestions found.</div>
          </div>
        ) : (
          workouts.map(workout => (
            <div key={workout.id} className="col-md-6 col-lg-4 mb-4">
              <div className="card h-100 shadow-sm">
                <div className="card-header bg-primary text-white">
                  <h5 className="card-title mb-0">{workout.name}</h5>
                </div>
                <div className="card-body">
                  <p className="card-text mb-3">{workout.description}</p>
                  <ul className="list-group list-group-flush mb-3">
                    <li className="list-group-item"><strong>Difficulty:</strong> 
                      <span className={`badge ms-2 ${
                        workout.difficulty_level === 'Beginner' ? 'bg-success' :
                        workout.difficulty_level === 'Intermediate' ? 'bg-warning' :
                        'bg-danger'
                      }`}>{workout.difficulty_level}</span>
                    </li>
                    <li className="list-group-item"><strong>Duration:</strong> {workout.duration} minutes</li>
                    <li className="list-group-item"><strong>Category:</strong> {workout.category || 'N/A'}</li>
                  </ul>
                  {workout.instructions && (
                    <div className="alert alert-light">
                      <strong>Instructions:</strong>
                      <p className="mb-0 mt-2 small">{workout.instructions}</p>
                    </div>
                  )}
                </div>
                <div className="card-footer">
                  <button className="btn btn-primary btn-sm w-100">Start Workout</button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default Workouts;
