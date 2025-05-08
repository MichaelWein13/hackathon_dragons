async function fetchData() {
    const res=await fetch ("https://api.coronavirus.data.gov.uk/v1/data");
    const record=await res.json();
    document.getElementById("date").innerHTML=record.data[0].date;
    document.getElementById("areaName").innerHTML=record.data[0].areaName;
    document.getElementById("latestBy").innerHTML=record.data[0].latestBy;
    document.getElementById("deathNew").innerHTML=record.data[0].deathNew;
    console.log('uooo');
    (async () => {
        // see the note below on how to choose currentWindow or lastFocusedWindow
        const [tab] = await chrome.tabs.query({active: true, lastFocusedWindow: true});
        console.log(tab.url);
        // ..........
      })();
}
fetchData();