let mockData = {}; // Global variable

async function loadRealData() {
    return new Promise((resolve, reject) => {
        Papa.parse('data/sony_cleaned_data.csv', {
            download: true,
            header: true,
            skipEmptyLines: true,
            complete: function(results) {
                const rows = results.data;
                const productGroups = {};
                
                rows.forEach(r => {
                    if (!r.product) return;
                    if (!productGroups[r.product]) productGroups[r.product] = [];
                    productGroups[r.product].push(r);
                });

                const productsList = [];
                const featureInsights = {};
                let totalSentiment = 0;
                const recentComments = [];

                Object.keys(productGroups).forEach(prodName => {
                    const group = productGroups[prodName];
                    const id = prodName.toLowerCase().replace(/[^a-z0-9]/g, '');
                    
                    // The CSV does not contain sentiment. We'll pseudo-generate it for the scaffold.
                    let groupSentiment = Math.floor(50 + (group.length % 40)); 
                    totalSentiment += groupSentiment;
                    let risk = groupSentiment > 75 ? 'Low' : (groupSentiment > 60 ? 'Medium' : 'High');

                    productsList.push({
                        id: id,
                        name: prodName,
                        sentimentScore: groupSentiment,
                        reviewVolume: group.length,
                        backlashRisk: risk,
                        revenue: "N/A",
                        trend: group.length > 20 ? "+5%" : "-2%"
                    });

                    featureInsights[id] = {
                        battery: Math.floor(Math.random() * 30) + 50,
                        sound: Math.floor(Math.random() * 30) + 50,
                        price: Math.floor(Math.random() * 30) + 50,
                        comfort: Math.floor(Math.random() * 30) + 50,
                        durability: Math.floor(Math.random() * 30) + 50
                    };

                    group.slice(0, 5).forEach(r => {
                        let text = r.clean_text || '';
                        if(text.length > 150) text = text.substring(0, 150) + '...';
                        recentComments.push({
                            product: id,
                            text: text,
                            sentiment: groupSentiment > 65 ? "Positive" : "Negative",
                            feature: r.source || 'General'
                        });
                    });
                });

                const avg = Math.floor(totalSentiment / Math.max(1, productsList.length));
                let lowestProd = productsList.sort((a,b) => a.sentimentScore - b.sentimentScore)[0];

                mockData = {
                    overview: {
                        totalReviews: rows.length,
                        avgSentiment: avg,
                        backlashMetric: lowestProd ? `High Risk: ${lowestProd.name}` : "Stable",
                        systemRecommendation: lowestProd ? `Investigate ${lowestProd.name}` : "Maintain Portfolio"
                    },
                    products: productsList,
                    featureInsights: featureInsights,
                    recentComments: recentComments,
                    keywordTags: {
                        positive: ["sony quality", "good performance", "reliable", "premium"],
                        negative: ["expensive", "glitches", "poor support", "outdated"],
                        mixed: ["decent", "average value", "fair"]
                    }
                };
                
                resolve();
            },
            error: function(err) {
                console.error("Error parsing CSV:", err);
                resolve(); // Fallback to avoid crashing
            }
        });
    });
}
window.loadRealData = loadRealData;
